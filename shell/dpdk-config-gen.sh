#!/bin/bash
#
# generate a string with given parameter lists

# Author: Yanan Zhao
# Date  : 2016-03-14

portlist=(0 1)
corelist=(2 4 6 8)

# final config string
config="--config=\""

for portid in ${portlist[@]}
do
    queueid=0

    for coreid in ${corelist[@]}
    do
        # echo "(portid, queueid, coreid): " $portid $queueid $coreid
        config=$config"("$portid","$queueid","$coreid"),"
        queueid=$(($queueid+1))
    done
done

# replace last character "," with "\""
configlen=${#config}
config=${config:0:$(($configlen-1))}"\""
echo $config # output: --config="(0,0,2),(0,1,4),(0,2,6),(0,3,8),(1,0,2),(1,1,4),(1,2,6),(1,3,8)"
