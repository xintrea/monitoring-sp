# -*- coding: utf-8 -*-

import time
import sqlite3

from Log import *
from Monitoring import *


class SituationFilter():

  def __init__(self):
    self.dbFileName=""


  # Запоминание файла БД, в котором хранятся ситуации
  def setDbFileName(self, fileName):
    self.dbFileName=fileName


  # Запоминание ситуации в БД
  def save(self, valueName, ruleName):
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()

    sql='INSERT INTO situation (valueName, ruleName, timeStamp) VALUES ( "'+valueName+'", "'+ruleName+'", strftime("%s", "now") )'

    # print('Class : '+__name__+' : Value insert command '+sql)

    cursor.execute(sql)
    
    cursor.close()
    db.commit();
    db.close()
 
    
  # Получение времени последней ситуации с указанными valueName и ruleName из БД
  def getTimeStampForLastSituation(self, valueName, ruleName):
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()

    sql='SELECT timeStamp FROM situation WHERE valueName="'+valueName+'" AND ruleName="'+ruleName+'"ORDER BY id DESC LIMIT 1'

    # print('Class : '+__name__+' : Select value command '+sql)

    cursor.execute(sql)

    result = cursor.fetchone()

    cursor.close()
    db.commit()
    db.close()
    
    if result==None or result=='None':
      return None
    else:  
      return int(result[0])


    