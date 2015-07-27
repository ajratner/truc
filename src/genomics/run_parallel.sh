#!/bin/sh
set -eu

if [ "$#" -le 4 ]; then
  echo "Usage: $0 [python_script] [input_file] [parallelism] [batch_size] [output_file]"
  echo "Where [python_script] should satisfy the following spec:"
  echo " INPUT: lines into sys.stdin"
  echo " OUTPUT: lines printed out"
  exit
fi
SCRIPT=$1
INPUT_FILE=$2
PARALLELISM=$3
BATCH_SIZE=$4
OUTPUT_FILE=$5
mkdir -p ${OUTPUT_FILE}.split
rm -f ${OUTPUT_FILE}.split/*

echo "[MAP] Splitting input file..."
split -a 10 -l ${BATCH_SIZE} ${INPUT_FILE} ${OUTPUT_FILE}.split/input-

echo "[EXECUTE] Executing run.sh in parallel..."
find ${OUTPUT_FILE}.split -name "input-*" 2>/dev/null -print0 | xargs -0 -P $PARALLELISM -L 1 ./run.sh ${SCRIPT}

echo "[REDUCE] Concatenating to output file..."
cat ${OUTPUT_FILE}.split/*.processed > ${OUTPUT_FILE}

echo "[CLEANUP] Removing intermediate files..."
rm -rf ${OUTPUT_FILE}.split/
