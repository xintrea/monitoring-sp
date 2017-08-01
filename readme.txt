Dependency
----------

Python
SCMXX - for send SMS message by COM-port


How to use
----------


1. Create empty SQLite3 database:

sqlite3 database.db


2. Run create tables commands in SQLite3 console:

.read dbcreate.sql


3. Set parameters in Monitoring.py


4. Run Monitoring.py in python:

/usr/bin/python ./Monitoring.py


5. Write Monitoring.py periodic start in Cron config


