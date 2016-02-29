#!/bin/sh
mem_stat=`free -m / | awk '{print $4}' | head -n 2|tail -n1|sed 'N;s/\n//'`


if [ $mem_stat -gt 2 ]
then
    echo "OK size"
    exit 0
else
    echo "size !!!"
    sync; echo 3 > /proc/sys/vm/drop_caches
    exit 2
fi

