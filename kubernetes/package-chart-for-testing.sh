#!/bin/sh

# You can use this helper script to package a chart for testing in craystack or a test system
# Copyright 2020-2021, Hewlett Packard Enterprise Development LP

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
path_to_chart="$1"
if [ -z "$path_to_chart" ]; then
  echo "Provide a single argument that is the local path to the chart you want to package"
  exit 1
fi
path_to_chart=$( cd $path_to_chart >/dev/null 2>&1 && pwd )
chart_name=$(basename $path_to_chart)

docker run --rm -it -v $path_to_chart:/charts/$chart_name -v $this_dir:/packaged-dest \
  arti.dev.cray.com/csm-internal-docker-stable-local/craypc/chartsutil:latest \
  /bin/sh -c "cd /charts/$chart_name && helm dep up && helm package . -d /packaged-dest"
