#!/bin/bash

docker run -d \
           -p 3000:3000 \
           --restart unless-stopped \
           --name=grafana \
           --volume "/home/labadmin/data-grafana:/var/lib/grafana"  \
       grafana/grafana
