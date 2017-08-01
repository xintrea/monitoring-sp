# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE

import re
import time
import stat
import datetime


# Запуск внешней программы
def runCommand(cmd):
  p=Popen(cmd, stdout=PIPE, shell=True)
  stdOutData, stdErrData = p.communicate()
  errCode=p.returncode

  # Убирается последний перенос строк, чтобы в конце небыло пустой строки
  stdOutData=re.sub("\n$", '', str(stdOutData))
  stdErrData=re.sub("\n$", '', str(stdErrData))
  
  return(stdOutData, stdErrData, errCode)


# Запуск внешней команды, которая может зависнуть по I/O
def runHardCommand(cmd, waitTime):

  # Удаляется предыдущий исполнимый файл
  if os.path.exists('./run.sh'):
    os.remove('./run.sh')

  # Команды записываются в исполнимый файл
  fileDescriptor = open('./run.sh', 'w')
  fileDescriptor.write('#!/bin/sh'+"\n")
  fileDescriptor.write(cmd)
  fileDescriptor.close()

  os.chmod('./run.sh', stat.S_IRUSR | stat.S_IWUSR | stat.S_IEXEC)

  print "Запускаются команды во внешнем процессе:"
  print cmd+"\n"

  # Запускается выполнение команд
  errCode=os.system('./runHardProcess.sh '+str(waitTime))

  return errCode
