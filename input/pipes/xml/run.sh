#! /bin/bash
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 [INPUT_XML_DIR] [OUTPUT_JSON_FILE]"
  exit
fi
echo "Parsing $1, saving to $2"
java -ea -jar parser.jar $1 > $2
