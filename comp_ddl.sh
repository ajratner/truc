#! /bin/bash

export DEEPDIVE_HOME=`cd ../deepdive; pwd`

java -jar ${DEEPDIVE_HOME}/util/ddlog.jar compile app.ddl | sed -e 's/^\(.*\)\(style: "tsv_extractor"\)/\1\2XXNXX\1parallelism: 8/g' -e $'s/XXNXX/\\\n/g' > deepdive.conf
