Dependency
----------

1. Python
2. SQLite3
3. scmxx - SCMXX package for send SMS message by COM-port
4. snmp - SNMP client


How to use
----------


1. Create empty SQLite3 database. Run command:

sqlite3 database.db


2. ... and in SQLite3 console run create tables commands:

.read dbcreate.sql

For exit from SQLite console, use command ".q"


3. Set parameters in Config.py


4. Run Monitoring.py in python:

/usr/bin/python ./Monitoring.py


5. Insert Monitoring.py periodic start in Cron config


