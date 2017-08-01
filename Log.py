# -*- coding: utf-8 -*-

# Устранение проблем с кодировкой UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Log():

  def __init__(self):
    self.text=""
    self.fileName="/tmp/log.txt"


  # Установка файла лога
  def setFileName(self, fileName):
    self.fileName=fileName


  def echo(self, inputText):
    print inputText+"\n"

    f = open(self.fileName, 'at')
    f.write(inputText+"\n")
    f.close()

    self.text += inputText+"\n"


  def getAll(self):
    return self.text

log=Log()
