#!/bin/bash

docker run --rm \
      -e INFLUXDB_DB=db0 \
      -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=password \
      -e INFLUXDB_USER=telegraf -e INFLUXDB_USER_PASSWORD=password \
      -v /home/labadmin/influxdb-data:/var/lib/influxdb \
      influxdb /init-influxdb.sh