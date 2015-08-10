#! /bin/bash

export DBTYPE=gp
export DBUSER=ajratner
export DBHOST=raiders2.stanford.edu
export DBPORT=6432
export DBNAME=tables

export GPPORT=8097
export GPHOST=$DBHOST

export ROOT_HOME=/lfs/local/0/ajratner
export DEEPDIVE_HOME=${ROOT_HOME}/deepdive_0_6
export APP_HOME=${ROOT_HOME}/truc

export PYTHONPATH=$PYTHONPATH:/lfs/local/0/ajratner/packages/lib/python2.7/site-packages

export PATH="/dfs/scratch1/netj/wrapped/greenplum:$PATH"
export GPPATH=/lfs/local/0/$DDUSER/data/gp_data
export GPHOME=/lfs/local/0/senwu/software/greenplum/greenplum-db
export OPENSSL_CONF=$GPHOME/etc/openssl.cnf

export PYTHONPATH=$PYTHONPATH:$DEEPDIVE_HOME/ddlib:$DEEPDIVE_HOME/ddlib/ddlib
export PYTHONPATH=$PYTHONPATH:$REAL_DIRNAME/analysis/util
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DEEPDIVE_HOME/lib/dw_linux/lib:$DEEPDIVE_HOME/lib/dw_linux/lib64
export PATH=$PATH:$DEEPDIVE_HOME/ddlib:$DEEPDIVE_HOME/sbt
