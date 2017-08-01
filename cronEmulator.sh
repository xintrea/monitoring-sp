#!/bin/sh

 

# Cron Emulator v.0.1

# © Sergey M. Stepanov 2013, xintrea@gmail.com, http://webhamster.ru

# License: GPL v.3

 

userName=`whoami`

 

echo "Variable names:"

list=`export | sed 's/^export //' | sed 's/=.*//'`

echo $list

 

echo "Remove all variables"

for line in $list

do

 echo "Remove variable: $line"

 unset $line

done

 

export HOME="/home/${userName}"

export LOGNAME="${userName}"

export OLDPWD="/home/${userName}"

export PATH="/usr/bin:/bin"

export PWD="/home/${userName}"

export SHELL="/bin/sh"

export SHLVL="1"

export USER="${userName}"

 

echo "User variable set:"

export

 

echo "Run examine commands..."

 

# Examine commands

 

/usr/bin/python /opt/monitoring/Monitoring.py
