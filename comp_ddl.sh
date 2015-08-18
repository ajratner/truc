#! /bin/bash

export DEEPDIVE_HOME=`cd ../deepdive; pwd`

source env_local.sh

java -jar ${DEEPDIVE_HOME}/util/ddlog.jar compile app.ddl | sed -e 's/^\(.*\)\(style: "tsv_extractor"\)/\1\2XXNXX\1parallelism: 40/g' -e $'s/XXNXX/\\\n/g' > deepdive.conf

echo "deepdive.inference.parallel_grounding: ${PARALLEL_GROUNDING}" >> deepdive.conf
echo "deepdive.db.default.gphost: $GPHOST" >> deepdive.conf
echo "deepdive.db.default.gpport: $GPPORT" >> deepdive.conf
echo "deepdive.db.default.gppath: $GPPATH" >> deepdive.conf
