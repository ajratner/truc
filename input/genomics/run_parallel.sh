#!/bin/sh
set -eu

if [ "$#" -le 3 ]; then
  echo "Usage: $0 [input_file] [parallelism] [batch_size] [output_dir]"
  echo "This script references a run.sh script which should satisfy the following spec:"
  echo " INPUT: a filepath f"
  echo " OUTPUT: a file f.processed"
  exit
fi
INPUT_FILE=$1
PARALLELISM=$2
BATCH_SIZE=$3
OUTPUT_FILE=$4
mkdir -p ${OUTPUT_FILE}.split
rm -f ${OUTPUT_FILE}.split/*

echo "[MAP] Splitting input file..."
split -a 10 -l ${BATCH_SIZE} ${INPUT_FILE} ${OUTPUT_FILE}.split/input-

echo "[EXECUTE] Executing run.sh in parallel..."
find ${OUTPUT_FILE}.split -name "input-*" 2>/dev/null -print0 | xargs -0 -P $PARALLELISM -L 1 ./run.sh

echo "[REDUCE] Concatenating to output file..."
cat ${OUTPUT_FILE}.split/*.processed > ${OUTPUT_FILE}

echo "[CLEANUP] Removing intermediate files..."
rm -rf ${OUTPUT_FILE}.split/
