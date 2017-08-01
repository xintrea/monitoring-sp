# -*- coding: utf-8 -*-

import time
import sqlite3

from Log import *
from Monitoring import *


class MeasureValue():

  def __init__(self):
    # Список описаний значений
    self.items={}


  # Добавление описания значения
  def addItem(self, 
              valueName='',
              valueType='', # "Возможные значения 'int', 'float', 'str'
              valueSubType='', # Возможные значения 'snmpDeviceSensor', 'pingTest', 'icmpCountFrom5'
              address='',
              id=''):
    
    # Проверка входных данных
    if not (valueType=='int' or valueType=='float' or valueType=='str') :
      print('Class : '+__name__+' : Cant add measure value with unknown type '+valueType)
      return False

    # Проверка входных данных
    if not (valueSubType=='snmpDeviceSensor' or valueSubType=='pingTest' or valueSubType=='icmpCountFrom5') :
      print('Class : '+__name__+' : Cant add measure value with unknown sub-type '+valueSubType)
      return False
      
    # Запоминание описания значения
    valueDesc={"type":valueType, 
               "subType":valueSubType, 
               "address":address, 
               "id":id}
    self.items[valueName]=valueDesc

    return True


  # Запоминание файла БД, в котором хранятся значения
  def setDbFileName(self, fileName):
    self.dbFileName=fileName
    
    # Проверяется наличие таблицы в БД, и если таковой нет она создается
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()
    sql="""
        CREATE TABLE IF NOT EXISTS measureValue(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          valueName TEXT,
          valueData TEXT,
          timeStamp TEXT
        )
        """
    cursor.execute(sql)

    cursor.close()
    db.close()


  # Получение списка имен значений
  def getValuesName(self):
    nameList=[]
    for key in self.items.keys():
      nameList.append(key)
    return nameList


  # Запоминание значения в БД
  def saveValue(self, valueName, valueData):
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()

    # timeStamp=int(time.time())

    sql='INSERT INTO measureValue (valueName, valueData, timeStamp) VALUES ( "'+valueName+'", "'+valueData+'", strftime("%s", "now") )'

    # print('Class : '+__name__+' : Value insert command '+sql)

    cursor.execute(sql)
    
    cursor.close()
    db.commit();
    db.close()


  # Получение типа значения по имени значения
  def getValueType(self, valueName):

    # Если запрошенной переменной не существует
    if not (valueName in self.items) :
      return False
    else:
      return self.items[valueName]["type"]


  # Получение под-типа значения по имени значения
  def getValueSubType(self, valueName):

    # Если запрошенной переменной не существует
    if not (valueName in self.items) :
      return False
    else:
      return self.items[valueName]["subType"]


  # Преобразование значения в нужный тип
  def convertValueToOwnType(self, valueName, value):
    try: 
      if self.items[valueName]["type"]=="int":
        return int(value)
      if self.items[valueName]["type"]=="float":
        return float(value)
      if self.items[valueName]["type"]=="str":
        return str(value)
    except:    
      return None 


  # Получение текущего значения датчика
  def getCurrentValue(self, valueName):

    # Если запрошенной переменной не существует
    if not (valueName in self.items) :
      # print('Class : '+__name__+' : Cant find value with name '+valueName)
      return None

    result=None
    
    # Если запрашиваемое значение получается из устройства по протоколу SNMP
    if self.items[valueName]["subType"]=="snmpDeviceSensor" :
      cmd='/usr/bin/snmpget -c public -v 1 '+self.items[valueName]["address"]+' '+self.items[valueName]["id"]
      stdOutData, stdErrData, errCode=runCommand(cmd)
      if errCode!=0 :
        return None
      if len(stdOutData)==0 :
        return None
      else :
        result=(stdOutData.split())[-1] # Последнее слово в строке - это значение температурного датчика

      
    # Если запрашивается результат ping-теста (среднее время ответа в миллисекундах)
    if self.items[valueName]["subType"]=="pingTest" :
      # cmd='(/usr/bin/traceroute '+self.items[valueName]["address"]+' && /bin/ping -c 1 -W 3 '+self.items[valueName]["address"]+') | /bin/grep "bytes from" | /bin/grep "time" | /usr/bin/cut -d" " -f7 | /usr/bin/cut -d"=" -f2'
      cmd='/bin/ping -c 1 -W 3 '+self.items[valueName]["address"]+' | /bin/grep "bytes from" | /bin/grep "time" | /usr/bin/cut -d" " -f7 | /usr/bin/cut -d"=" -f2'

      # log.echo(cmd)
      
      stdOutData, stdErrData, errCode=runCommand(cmd)
      if errCode!=0 :
        return None
      if len(stdOutData)==0 :
        return None
      else :
        result=stdOutData

    # Если запрашивается результат подсчета прохождения пакетов из 5 ICMP пакетов (через ping)
    if self.items[valueName]["subType"]=="icmpCountFrom5" :
      cmd='/bin/ping -c 5 -W 3 '+self.items[valueName]["address"]+' | /bin/grep "bytes from '+self.items[valueName]["address"]+'" | wc -l'
      stdOutData, stdErrData, errCode=runCommand(cmd)
      if errCode!=0 :
        return None
      if len(stdOutData)==0 :
        return None
      else :
        result=stdOutData


    return self.convertValueToOwnType(valueName, result)
 
    
  # Получение последнего запомненного значения из БД
  def getLastSaveData(self, valueName, fields):
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()

    sql='SELECT '+fields+' FROM measureValue WHERE valueName="'+valueName+'" ORDER BY id DESC LIMIT 1'

    # print('Class : '+__name__+' : Select value command '+sql)

    cursor.execute(sql)

    result = cursor.fetchone()

    cursor.close()
    db.commit()
    db.close()
    
    if result==None or result=='None':
      return None
    else:  
      return result[0]


  # Получение пред-последнего запомненного значения из БД
  def getPreviousSaveData(self, valueName, fields):
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()

    sql='SELECT '+fields+' FROM measureValue WHERE valueName="'+valueName+'" ORDER BY id DESC LIMIT 2'

    # print('Class : '+__name__+' : Select value command '+sql)

    cursor.execute(sql)

    data = cursor.fetchall()
    
    if len(data)<=1:
      result=None
    else:
      row=data[1]
      if len(row)==1:
        result=row[0]
      else:
        result=row

    cursor.close()
    db.commit()
    db.close()
    
    if result==None or result=='None':
      return None
    else:  
      return result


  def getLastSaveValue(self, valueName):
    value=self.getLastSaveData(valueName, "valueData")
    return self.convertValueToOwnType(valueName, value)


  def getLastSaveTimeStamp(self, valueName):
    value=self.getLastSaveData(valueName, "timeStamp")
    return int(value)


  def getPreviousSaveValue(self, valueName):
    value=self.getPreviousSaveData(valueName, "valueData")
    return self.convertValueToOwnType(valueName, value)


  def getPreviousSaveTimeStamp(self, valueName):
    value=self.getPreviousSaveData(valueName, "timeStamp")
    return int(value)

    