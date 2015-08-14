#! /bin/bash

export DEEPDIVE_HOME=`cd ../deepdive; pwd`

java -jar ${DEEPDIVE_HOME}/util/ddlog.jar compile app.ddl > deepdive.conf
