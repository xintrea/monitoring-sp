# -*- coding: utf-8 -*-

import serial
from messaging.sms import SmsSubmit

from Log import *
from Helper import *


class SmsSender() :

  def __init__(self):
    self.reportPhoneNumber = () # Перечень телефонных номеров, куда нужно отправлять SMS
    self.mobileTty=""           # Устройство COM-порта мобильного телефона

  def setReportPhoneNumber(self, inputValue):
    # Если передана одна строка а не кортеж, строка преобразуется в кортеж
    if isinstance( inputValue, str ):
      self.reportPhoneNumber=( inputValue, )
    else:
      self.reportPhoneNumber=inputValue


  def setMobileTty(self, inputValue):
    self.mobileTty=inputValue


  # Отправка SMS сообщения
  def send(self, text):

    # Настройка терминала, похоже что без этой настройки ничего нормально работать не будет
    # cmdTtySetup='stty -F '+self.mobileTty+' raw ispeed 9600 ospeed 9600 ; '

    for currentPhoneNumber in self.reportPhoneNumber:
   
      if len(currentPhoneNumber)==0:
        continue
    
      log.echo("Отправляется SMS на номер "+currentPhoneNumber)

      cmd="/usr/bin/scmxx --device "+self.mobileTty+" --number "+currentPhoneNumber+" --text '"+text+"' --send --sms --direct --unicode"
      log.echo(cmd)
      stdOutData, stdErrData, errCode=runCommand(cmd)
      log.echo(stdOutData)
   
    return True
