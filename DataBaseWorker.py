# -*- coding: utf-8 -*-

import time
import sqlite3

from Log import *
from Monitoring import *


class DataBaseWorker():

  def __init__(self):
    self.dbFileName=""


  # Запоминание файла БД
  def setDbFileName(self, fileName):
    self.dbFileName=fileName
    
    # Проверяется наличие таблицы в БД, и если таковой нет она создается
    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()
    sql="""
        CREATE TABLE IF NOT EXISTS situation(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          valueName TEXT,
          ruleName TEXT,
          timeStamp TEXT
        )
        """
    cursor.execute(sql)

    cursor.close()
    db.commit();
    db.close()


  # Удаление устаревших данных в БД
  def deleteOlderData(self, dataOlderDeltaTime):

    currentTime=int( time.time() )
    edgeTime=str( currentTime-dataOlderDeltaTime )


    db = sqlite3.connect(self.dbFileName)
    cursor = db.cursor()

    sql='DELETE FROM situation WHERE timeStamp < '+edgeTime
    cursor.execute(sql)

    sql='DELETE FROM measureValue WHERE timeStamp < '+edgeTime
    cursor.execute(sql)

    sql='VACUUM'
    cursor.execute(sql)

    cursor.close()
    db.commit();
    db.close()
