#!/bin/sh
#
# exclude annoying dirs and files on grep
#
# Author: Yanan Zhao
# Date  : 2017-01-07 17:18:48

grep -R --color=always --exclude=tags --exclude-dir=tests \
    --exclude-dir=datapath-windows \
    --exclude-dir=ovn \
    --exclude-dir=xenserver \
    "$@"
