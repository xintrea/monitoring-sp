# -*- coding: utf-8 -*-

import time
import datetime

from Log import *
from Helper import *
from Config import *
from MeasureValue import *
from MailSender import *
from SmsSender import *
from ValueAnalytic import *
from SituationFilter import *
from DataBaseWorker import *

def test(measureValue): pass # "Прототип" функции test - для отладки


#----------------
# Основные данные
#----------------

# Версия скрипта
version='0.35'

# Время старта скрипта
startTime=datetime.datetime.now().strftime( '%Y-%m-%d-%H-%M-%S' )


#-------------
# Основной код
#-------------

def main():

  # Объект конфигурации и заполняется основными настройками
  config.setMainProperties()

  log.setFileName(config.logFileName)
  log.echo("\n\n")
  log.echo('Мониторинг v.'+version)
  log.echo('Время запуска: '+startTime)
  log.echo("\n")

  # Подготовка базы данных
  dataBaseWorker=DataBaseWorker()
  dataBaseWorker.setDbFileName( config.dbFileName ) # Установка имени файла БД
  dataBaseWorker.deleteOlderData( config.dataOlderDeltaTime ) # Удаление устаревших данных

  # После подготовки базы данных можно подгружать настройки считываемых значений
  measureValue=config.getMeasureValue()
  valueAnalytic=config.getValueAnalytic()

  monitoringCycle(measureValue, valueAnalytic)

  return


def monitoringCycle(measureValue, valueAnalytic):  
  
  # Проверка работоспособности класса MeasureValue
  # test(measureValue)
  # return

  # Считывание текущих значений датчиков и их запись
  for valueName in measureValue.getValuesName():
    v=str(measureValue.getCurrentValue( valueName ))
    log.echo("Значение датчика "+valueName+"="+v)
    measureValue.saveValue( valueName, v )


  # Проверка значений и получение отчета если сработали правила
  rulesResult=valueAnalytic.checkAllRules( measureValue )

  if len( rulesResult )==0:
    log.echo('Все оборудование работает нормально, либо недавно уже было оповещение о проблемах');
  else:
    log.echo("\nВНИМАНИЕ !\nОбнаружены ошибки в работе оборудования.");

    # Отправка отчета по почте
    if config.sendMailFlag:
      mailSender=MailSender()
      mailSender.setReportMail(config.reportMail)
      mailSender.setMailFrom(config.mailFrom)
      mailSender.setMailServer(config.mailServer)
      mailSender.setMailPort(config.mailPort)
      mailSender.setMailUser(config.mailUser)
      mailSender.setMailPassword(config.mailPassword)
      mailSender.send('Monitoring report', startTime+"\n"+rulesResult+"\n"+log.getAll()) # По почте сообщение отправляется всегда
    
    # Отправка уведомлений по SMS
    if config.sendSmsFlag:

      # Количество секунд с начала дня
      currentTime = datetime.datetime.now()
      currentHour = currentTime.hour # Час текущий
      currentMinute = currentTime.minute # Минута текущая
      currentSecond = currentTime.second # Секунда текущие
      currentSecondInDay=currentSecond + currentMinute*60 + currentHour*60*60

      # Если не время молчания
      if currentSecondInDay>=config.muteSmsStartInDay and currentSecondInDay<=config.muteSmsStopInDay:
        smsSender=SmsSender()
        smsSender.setReportPhoneNumber(config.reportPhoneNumber)
        smsSender.setMobileTty(config.mobileTty)
        smsSender.send("Monitoring:\n"+rulesResult) # По SMS сообщение отправляется только не во время молчания

    # Обнаруженные ошибки пробрасываются в лог
    log.echo(rulesResult)

  log.echo('Мониторинг завершен.');

  return


# Отладка. Тестирование основной функциональности
def test(measureValue):

  # Получение текущих значений
  t1=str(measureValue.getCurrentValue("APC5000_Temperature"))
  t2=str(measureValue.getCurrentValue("APC1000_Temperature"))
  p1=str(measureValue.getCurrentValue("ms0_Ping"))

  log.echo("Get temperature APC5000: "+t1)
  log.echo("Get temperature APC1000: "+t2)
  log.echo("Get ping test ms0: "+p1)
  
  # Сохранение текущих значений
  log.echo("Save value... ")
  measureValue.saveValue("APC5000_Temperature", t1)
  measureValue.saveValue("APC1000_Temperature", t2)
  measureValue.saveValue("ms0_Ping", p1)
  log.echo("Saving.")

  t1cv=measureValue.getLastSaveValue("APC5000_Temperature")
  t1ct=measureValue.getLastSaveTimeStamp("APC5000_Temperature")
  log.echo("Last save value APC5000_Temperature: "+str(t1cv))
  log.echo("Last save timestamp APC5000_Temperature: "+str(t1ct))
  if t1!=t1cv:
    log.echo("Ошибка! Последнее значение не соответствует последнему сохраненному значению")

  t2cv=measureValue.getLastSaveValue("APC1000_Temperature")
  t2ct=measureValue.getLastSaveTimeStamp("APC1000_Temperature")
  log.echo("Last save value APC1000_Temperature: "+str(t2cv))
  log.echo("Last save timestamp APC1000_Temperature: "+str(t2ct))
  if t2!=t2cv:
    log.echo("Ошибка! Последнее значение не соответствует последнему сохраненному значению")

  # Предыдущие значения
  t1pv=measureValue.getPreviousSaveValue("APC5000_Temperature")
  t1pt=measureValue.getPreviousSaveTimeStamp("APC5000_Temperature")
  log.echo("Previous save value APC5000_Temperature: "+str(t1pv))
  log.echo("Previous save timestamp APC5000_Temperature: "+str(t1pt))

  t2pv=measureValue.getPreviousSaveValue("APC1000_Temperature")
  t2pt=measureValue.getPreviousSaveTimeStamp("APC1000_Temperature")
  log.echo("Previous save value APC1000_Temperature: "+str(t2pv))
  log.echo("Previous save timestamp APC1000_Temperature: "+str(t2pt))

  return


# Конструкция чтобы работала функция main()
if __name__ == '__main__':
  main()


