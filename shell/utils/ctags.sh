#!/bin/sh
#
# generate tags for C/C++ projects, exclude specific dirs and files
#
# Author: Yanan Zhao
# Date  : 2017-01-07 17:18:48

ctags -R --languages=C,C++ \
    --exclude=build-aux \
    --exclude=datapath-windows \
    --exclude=Documentation \
    --exclude=python \
    --exclude=tests \
    --exclude=third-party \
    --exclude=windows \
    --exclude=xenserver \
    *
