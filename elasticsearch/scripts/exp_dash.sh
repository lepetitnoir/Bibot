#!/bin/bash

if [ -z "$1" ]
  then
    echo "Missing path to dashboard file!"
    exit 1
fi

FILENAME=$1
curl -X POST "http://localhost:5601/api/saved_objects/_export" -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d '
{
  "type": "dashboard",
  "includeReferencesDeep": true
}' > "${FILENAME}"


