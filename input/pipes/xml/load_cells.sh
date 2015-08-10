#! /bin/bash

source ../../../env_local.sh

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 [INPUT: input file] [table_name]"
  exit
fi

INPUT=$1
TABLE=$2

echo "Copying $INPUT into $DBNAME.$TABLE"
cat $INPUT | psql -U $DBUSER -h $DBHOST -p $DBPORT $DBNAME -X --set ON_ERROR_STOP=1 -c "COPY $TABLE FROM STDIN"

echo "Done."
