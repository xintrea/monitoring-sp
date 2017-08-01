# -*- coding: utf-8 -*-

import smtplib
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate

from Log import *


class MailSender() :

  def __init__(self):
    self.reportMail = () # Перечень email-адресов, куда нужно отправлять почту
    self.mailFrom=""     # Email-адрес, с которого происходит отправка письма
    self.mailServer=""   # Адрес SMTP сервера, используемого для отправки письма
    self.mailPort=25     # Порт
    self.mailUser=""     # Логин пользователя почтового сервера
    self.mailPassword="" # Пароль пользователя почтового сервера

  def setReportMail(self, inputValue):
    # Если передана одна строка а не кортеж, строка преобразуется в кортеж
    if isinstance( inputValue, str ):
      self.reportMail=( inputValue, )
    else:
      self.reportMail=inputValue

  def setMailFrom(self, inputValue):
    self.mailFrom=inputValue

  def setMailServer(self, inputValue):
    self.mailServer=inputValue

  def setMailPort(self, inputValue):
    self.mailPort=inputValue

  def setMailUser(self, inputValue):
    self.mailUser=inputValue

  def setMailPassword(self, inputValue):
    self.mailPassword=inputValue


  # Отправка почтового сообщения на почтовые адреса
  def send(self, title, text):

    msg = MIMEMultipart()
    msg["From"] = self.mailFrom
    msg["Subject"] = title
    msg['Date']    = formatdate(localtime=True)

    msg.add_header('X-Mailer', 'Monitoring mailer')
    msg.add_header('Content-type', 'text/html charset=utf-8')

    # Добавление текста сообщения
    msg.attach(MIMEText(text))

    for currentReportMail in self.reportMail:

      if len(currentReportMail)==0:
        continue

      log.echo("Отправляется письмо на почтовый ящик "+currentReportMail)

      if len(str(msg["To"]))>0 :
        del msg["To"]
        msg["To"] = currentReportMail

      try:
        # Подключение
        server = smtplib.SMTP(self.mailServer, self.mailPort)
        server.ehlo()
        server.starttls()
        server.ehlo()
        # Авторизация
        server.login(self.mailUser, self.mailPassword)
        # Отправка письма
        server.sendmail(msg["From"], currentReportMail, msg.as_string())
        server.quit()

        log.echo("Письмо на почтовый ящик "+currentReportMail+" успешно отправлено")

      except Exception, e:
        errorMsg = "Невозможно отправить письмо на почтовый ящик "+currentReportMail+". Error: %s" % str(e)
        log.echo(errorMsg)
