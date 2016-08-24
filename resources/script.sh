#!/bin/sh
ps -eaf 
max=30; while ! wget --http-user=aurin --http-password=aurin --spider --no-check-certificate https://localhost:443/geoserver > /dev/null 2>&1; do max=$(( max - 1 )); [ $max -lt 0 ] && break; sleep 5; done; [ $max -gt 0 ];

