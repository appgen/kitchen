#!/bin/sh
# Upload comestibles
set -e

if test -d comestibles; then
  for geojson in $(ls comestibles|grep .geojson); do
    seed=$(echo "$geojson"|sed 's/\.geojson\(\.gz\)$//')
    for extension in json csv geojson; do
      if test -f "comestibles/$seed.$extension" && ! test -f "comestibles/$seed.$extension.gz"; then
        gzip "comestibles/$seed.$extension"
      fi
      s3cmd put "comestibles/$seed.$extension.gz" s3://comestibles.appgen.me/"$seed.$extension" --add-header=Content-Encoding:gzip
    done
  done
else
  echo I can\'t find the comestibles directory.
fi
