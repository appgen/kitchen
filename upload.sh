#!/bin/sh
# Upload comestibles
set -e

for json in comestibles/*.json
  seed=$(basename $json .json)
  for extension in json csv geojson; do
    if test -f -- "$seed.$extension" && ! test -f -- "$seed.$extension"; then
      gzip "$seed.$extension"
    fi
    s3cmd put "$seed.$extension.gz" s3://comestibles.appgen.me/"$seed.$extension"
  done
done
