#!/bin/bash

folder=/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-best

lines=`ls $folder | wc -l`
echo $lines

batch=`expr $lines / 20`

echo $batch

for i in {0..19}
do
    echo "deleting old outputs"
    rm -rf outputs_pipeline$i
    mkdir outputs_pipeline$i
    
    echo "regenerating file list $i"
    cellprofiler -p pipeline.cpproj -i $folder -o outputs_pipeline$i
done

for i in {0..19}
#i=0
do
    let start=$i*$batch
    if [ $start = 0 ]; then
	start=1
    fi

    let end=($i+1)*$batch
    if [ $i = 19 ]; then
	end=$lines
    fi
    
    echo "starting task$i"
    cellprofiler -p outputs_pipeline$i/Batch_data.h5 -cr -f $start -l $end > outputs_pipeline$i/log.log 2>&1 &
done

