#!/bin/bash

file=$1

lines=`cat $file | wc -l`
echo $lines

batch=`expr $lines / 20`


for i in {0..19}
do
    let start=$i*$batch
    if [ $start = 0 ]; then
	start=1
    fi
    let end=($i+1)*$batch
    if [ $i = 19 ]; then
	end=$lines
    fi
    rm -rf outputs$i
    mkdir outputs$i
    echo "regenerating file list $i"
    cellprofiler -p check_cells.cpproj --file-list $file -o outputs$i
    echo "starting task$i"

    cellprofiler -p outputs$i/Batch_data.h5 -cr -f $start -l $end > outputs$i/log.log &
done
