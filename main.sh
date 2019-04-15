#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

IP=$(awk -F "=" '/IP/ {print $2}' config.ini)
PORT=$(awk -F "=" '/PORT/ {print $2}' config.ini)

$DIR/web/run.sh $IP:$PORT
