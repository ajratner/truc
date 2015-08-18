#! /bin/bash

source env_local.sh

# Launch gpfdist if not launched.
gpfdist -d $GPPATH -p $GPPORT &
gpfdist_pid=$!
trap "kill $gpfdist_pid" EXIT

deepdive run endtoend
