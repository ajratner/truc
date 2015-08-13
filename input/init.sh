#!/usr/bin/env bash
set -eux
cd "$(dirname "$0")"

CELLS=data/cells.tsv
echo "Loading from $CELLS"
cat $CELLS | deepdive sql "COPY cells FROM STDIN"
