# -*- coding: utf-8 -*-

# Устранение проблем с кодировкой UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from Log import *

# ----------------------------
# Конфигурирование мониторинга
# ----------------------------

class Config():

  def __init__(self):
    log.echo('Создание конфигурации')


  def setMainProperties(self):

    log.echo('Конфигурация: применение основных настроек')
    
    # Включение/выключение отправки сообщений. Используется при отправке
    self.sendSmsFlag=True
    self.sendMailFlag=True
    
    # Емайл для отправки отчетов
    self.reportMail=( 'adminsupermail@mail.ru', 'mybestmail@gmail.com' )
    
    # Настройки почты, откуда будут отправляться письма
    self.mailFrom='monitor@myhost.local.lan'
    self.mailServer='10.153.0.14'
    self.mailPort=587
    self.mailUser='monitor'
    self.mailPassword='yourpassword'
    
    # Телефонные номера для отправки отчетов
    self.reportPhoneNumber=( '+79181212123', '+79281212124', '+79251212125' )
    
    # Настройки COM-порта подключенного мобильника
    self.mobileTty='/dev/ttyS0'
    
    # Сколько времени выдерживать после срабатывания такого же правила с таким же датчиком (в секундах)
    self.situationReportPause=3*60*60
    
    # Через сколько времени (в секундах) считать данные в БД устаревшими и удалять их
    self.dataOlderDeltaTime=60*60*24*7
    
    # Период молчания с 00:00 по 07:00 для SMS оповещений (в секундах дня)
    self.muteSmsStartInDay=0
    self.muteSmsStopInDay=60*60*7
    
    # Настройки базы данных
    self.dbFileName="/opt/monitoring/database.db"
    
    # Настройка лога
    self.logFileName="/opt/monitoring/log.txt"


  def getMeasureValue(self):

    log.echo('Конфигурация: применение настроек измеряемых значений')

    # Настройка объекта для работы с измеряемыми значениями
    measureValue=MeasureValue()
    measureValue.setDbFileName(self.dbFileName) # Установка имени файла БД, где хранятся измеренные значения
    
    measureValue.addItem("APC5000_Temperature",            # Имя значения
                         "int",                            # Тип значения 
                         "snmpDeviceSensor",               # Механизм получения
                         "10.153.0.88",                    # IP устройства, откуда вытягивается значение 
                         ".1.3.6.1.4.1.318.1.1.1.2.2.2.0") # Для механизма snmpDeviceSensor указывается SNMP адрес
                       
    measureValue.addItem("APC5000_InputVoltage",
                         "int", 
                         "snmpDeviceSensor",
                         "10.153.0.88",
                         ".1.3.6.1.4.1.318.1.1.1.3.2.1.0")
                       
    measureValue.addItem("domainConroller0_Ping",          # Имя значения
                         "float",                          # Тип значения (задержка в секундах с дробной частью)
                         "pingTest",                       # Механизм получения
                         "10.153.0.11")                    # IP устройства, откуда вытягивается значение 
    
    measureValue.addItem("gateWay0_IcmpCountFrom5",        # Имя значения
                         "int",                            # Тип значения
                         "icmpCountFrom5",                 # Механизм получения
                         "10.153.0.1")                     # IP устройства, откуда вытягивается значение 
    return measureValue                     


  def getValueAnalytic(self):

    log.echo('Конфигурация: применение настроек анализатора значений')

    valueAnalytic=ValueAnalytic()
    valueAnalytic.setDbFileName(self.dbFileName) # Установка БД, где хранятся срабатывания правил
    valueAnalytic.setSituationReportPause(self.situationReportPause)

    # Правила срабатывания оповещений
    valueAnalytic.addRule({"ruleName":"Датчик температуры ИБП APC5000 слишком горячий",
                           "ruleType":"aboveOrEqual",             
                           "valueName":"APC5000_Temperature",      
                           "targetValue":32})
    
    valueAnalytic.addRule({"ruleName":"Датчик температуры ИБП APC5000 отключился",
                           "ruleType":"equal",             
                           "valueName":"APC5000_Temperature",      
                           "targetValue":0})
    
    valueAnalytic.addRule({"ruleName":"Слишком быстрое повышение температуры на ИБП APC5000",
                           "ruleType":"gradient",             
                           "valueName":"APC5000_Temperature",      
                           "deltaTime":58,
                           "deltaValue":2})
    
    valueAnalytic.addRule({"ruleName":"На ИБП APC5000 нет входного напряжения питания",
                           "ruleType":"equal",             
                           "valueName":"APC5000_InputVoltage",      
                           "targetValue":0})
    
    valueAnalytic.addRule({"ruleName":"Долгий ответ сервера домена dc0 на пинги",
                           "ruleType":"aboveOrEqual",             
                           "valueName":"domainConroller0_Ping",      
                           "targetValue":500.0})
    
    valueAnalytic.addRule({"ruleName":"Сервер домена dc0 не отвечает на пинги",
                           "ruleType":"equal",             
                           "valueName":"domainConroller0_Ping",      
                           "targetValue":None})
    
    valueAnalytic.addRule({"ruleName":"Пропадают не менее 4 из 5 ICMP пакетов от шлюза igw0 (серверная)",
                           "ruleType":"lessOrEqual",
                           "valueName":"gateWay0_IcmpCountFrom5",
                           "targetValue":(5-1)}) 

    return valueAnalytic

config=Config()
