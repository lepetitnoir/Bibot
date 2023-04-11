#!/bin/bash

if [ -z "$1" ]
  then
    echo "Missing path to dashboard file!"
    exit 1
fi


FILENAME=$1
curl -X POST "http://localhost:5601/api/saved_objects/_import?createNewCopies=true" -H "kbn-xsrf: true" --form file=@"${FILENAME}"