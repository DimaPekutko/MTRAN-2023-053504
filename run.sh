#!/bin/sh

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

export PYTHONPATH=$SCRIPTPATH
python3 $SCRIPTPATH/interpreter $1 $2
