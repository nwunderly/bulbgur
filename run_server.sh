#!/bin/bash

if [ "$1" == "main" ]
then
  uvicorn --host 0.0.0.0 --port 9000 src.main:app

elif [ "$1" == "static" ]
then
  uvicorn --host 0.0.0.0 --port 9001 src.static:app

else
  exit 1
fi
