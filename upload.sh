#!/bin/sh
# Upload comestibles
set -e

for geojson in comestibles/*.geojson; do
  seed=$(basename $geojson .geojson)
  for extension in json csv geojson; do
    if test -f "./$seed.$extension" && ! test -f "./$seed.$extension.gz"; then
      gzip "./$seed.$extension"
    fi
    s3cmd put "./$seed.$extension.gz" s3://comestibles.appgen.me/"$seed.$extension" --add-header=Content-Encoding:gzip
  done
done
