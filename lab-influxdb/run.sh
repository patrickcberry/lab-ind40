#!/bin/bash

docker run -d -p 8086:8086 \
      -v /home/labadmin/data-influxdb/:/var/lib/influxdb \
      --name=influxdb \
      influxdb
