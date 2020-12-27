#!/bin/bash

docker run -d -p 8086:8086 \
      -v $PWD:/var/lib/influxdb \
      --name=influxdb \
      influxdb
