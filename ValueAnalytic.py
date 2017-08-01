# -*- coding: utf-8 -*-

import time
import sqlite3

from Log import *
from Monitoring import *
from SituationFilter import *


class ValueAnalytic():

  def __init__(self):
    # Список правил, по которым надо проверять значения
    self.rules=[]
    self.situationFilter=SituationFilter()
    self.situationReportPause=0


  def setDbFileName(self, fileName):
    self.situationFilter.setDbFileName(fileName)

    
  def setSituationReportPause(self, pause):
    self.situationReportPause=pause


  # Добавление описания правила
  # Возможные правила:
  #
  # {"ruleName":"Точное соответствие значению",
  #  "ruleType":"equal",
  #  "valueName":"APC5000_Temperature",
  #  "targetValue":15}
  #
  # {"ruleName":"Значение больше или равно",
  #  "ruleType":"aboveOrEqual",
  #  "valueName":"APC5000_Temperature",
  #  "targetValue":15}
  #
  # {"ruleName":"Значение меньше или равно",
  #  "ruleType":"lessOrEqual",
  #  "valueName":"APC5000_Temperature",
  #  "targetValue":15}
  #  
  # {"ruleName":"Градиент значения изменяется слишком быстро",
  #  "ruleType":"gradient",
  #  "valueName":"APC5000_Temperature",
  #  "deltaTime":60, # Здесь двумя параметрами deltaTime и deltaValue задается допустимый градиент
  #  "deltaValue":2}
  def addRule(self,
              rule={}):

    # Запоминание описания правила
    # ruleDesc={ "ruleName":ruleName, "valueType":valueType, "criticalDeltaTime":criticalDeltaTime, "criticalDeltaValue":criticalDeltaValue, "warningValue":warningValue }
    self.rules.append(rule)

    return True


  # Запуск на проверку всех правил
  def checkAllRules(self, measureValue):
    log.echo("Проверка изменений в значениях датчиков...")

    returnResult=""

    # Перебор правил
    for rule in self.rules:

      result=False
      resultData={'sensor':'',
                  'reason':'',
                  'situation':'',
                  'enableValue':'',
                  'currValue':''}
      
      currentValue=measureValue.getLastSaveValue( rule["valueName"] )
      currentTime=measureValue.getLastSaveTimeStamp( rule["valueName"] )
      
      previousValue=measureValue.getPreviousSaveValue( rule["valueName"] )
      previousTime=measureValue.getPreviousSaveTimeStamp( rule["valueName"] )
      
      # log.echo("Current v: "+str(currentValue)+" Current t: "+str(currentTime))
      # log.echo("Previous v: "+str(previousValue)+" Previous t: "+str(previousTime))
      
      if rule["ruleType"]=="equal":
        if currentValue==rule["targetValue"]:
          # result="Sensor: "+rule["valueName"]+"\nReason: Eq.\nSituation: "+rule["ruleName"]+"\nCurr. val.: "+str(currentValue)
          result=True
          resultData['sensor']=rule["valueName"]
          resultData['reason']='Eq.'
          resultData['situation']=rule["ruleName"]
          resultData['enableValue']=''
          resultData['currValue']=str(currentValue)
          
          
      if rule["ruleType"]=="aboveOrEqual":
        if currentValue>=rule["targetValue"]:
          # result="Sensor: "+rule["valueName"]+"\nReason: Above or eq.\nSituation: "+rule["ruleName"]+"\nEnable val.: "+str(rule["targetValue"])+"\nCurr. val.: "+str(currentValue)
          result=True
          resultData['sensor']=rule["valueName"]
          resultData['reason']='Above or eq.'
          resultData['situation']=rule["ruleName"]
          resultData['enableValue']=str(rule["targetValue"])
          resultData['currValue']=str(currentValue)

      if rule["ruleType"]=="lessOrEqual":
        if currentValue<=rule["targetValue"]:
          # result="Sensor: "+rule["valueName"]+"\nReason: Less or eq.\nSituation: "+rule["ruleName"]+"\nEnable val.: "+str(rule["targetValue"])+"\nCurr. val: "+str(currentValue)
          result=True
          resultData['sensor']=rule["valueName"]
          resultData['reason']='Less or eq.'
          resultData['situation']=rule["ruleName"]
          resultData['enableValue']=str(rule["targetValue"])
          resultData['currValue']=str(currentValue)
          
      if rule["ruleType"]=="gradient":
        if currentValue is None:
          currentValue=0
        if previousValue is None:
          previousValue=0
        deltaValue=int(currentValue)-int(previousValue)

        deltaTime=int(currentTime)-int(previousTime)

        if (deltaTime>=rule["deltaTime"] and deltaValue>=rule["deltaValue"]):

          # result="Sensor: "+rule["valueName"]+"\nReason: "+reason+"\nSituation: "+rule["ruleName"]+"\nEnable val.: "+str(rule["targetValue"])+"\nCurr.val: "+str(currentValue)

          result=True
          resultData['sensor']=rule["valueName"]
          resultData['situation']=rule["ruleName"]
          resultData['enableValue']=str(rule["targetValue"])
          resultData['currValue']=str(currentValue)

          if deltaValue>=0:
            resultData['reason']="Unexpected value up"
          else:  
            resultData['reason']="Unexpected value down"
  
      
      # Если сработало правило
      if result==True:
        previousTimeStamp=self.situationFilter.getTimeStampForLastSituation(rule["valueName"], rule["ruleName"])
        currentTimeStamp = int(time.time())

        log.echo("Сработало правило: "+resultData['situation'])
        
        # Если ранее правило еще не срабатывало (есть превышение времени выжидания с момента появления такого же правила)
        if previousTimeStamp==None or (currentTimeStamp-previousTimeStamp)>self.situationReportPause:
          self.situationFilter.save(rule["valueName"], rule["ruleName"]) # Отмечается что правило сработало
          
          resultText=''
          if len(resultData['situation'])>0:
            resultText+='Situation: '+resultData['situation']+"\n"
          if len(resultData['sensor'])>0:
            resultText+='Sensor: '+resultData['sensor']+"\n"
          if len(resultData['enableValue'])>0:
            resultText+='Enable val.: '+resultData['enableValue']+"\n"
          if len(resultData['reason'])>0:
            resultText+='Reason: '+resultData['reason']+"\n"
          if len(resultData['currValue'])>0:
            resultText+='Curr. val.: '+resultData['currValue']+"\n"
          
          returnResult+=resultText+"\n"
        
    return returnResult
          
      
        
      
      