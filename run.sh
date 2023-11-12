#!/bin/bash

export $(grep -v '^#' .env | xargs -0)

container=statement-parser-dev-1
cmd="python3 main.py"

if ! [ -f /.dockerenv ]; then
  docker cp run.sh $container:/app
  docker cp .env $container:/app
  docker exec -it $container ./run.sh
else
  clear; time $cmd $sheet_key
  while true; do
    sleep 1
    n=`find . -type f -name '*.py' -mmin 0.0167 | wc -l`
    if [ "$n" -gt "0" ]; then
      clear; time $cmd $sheet_key
    fi
  done
fi
