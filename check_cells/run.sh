#!/bin/bash

folder=/media/af214dbe-b6fa-4f5e-932a-14b133ba4766/zhangya/svs-selected

file=filelist
rm $file
find $folder -name *.png > $file

lines=`cat $file | wc -l`
echo $lines

batch=`expr $lines / 20`
echo $batch
#batch=10

for i in {0..19}
#i=0
do
    echo "deleting old outputs"
    rm -rf outputs$i
    mkdir outputs$i
    
    echo "regenerating file list $i"
    cellprofiler -p check_cells.cpproj --file-list $file -o outputs$i
done
for i in {0..19}
do
    echo "starting task$i"
    let start=$i*$batch
    if [ $start = 0 ]; then
	start=1
    fi
    let end=($i+1)*$batch
    if [ $i = 19 ]; then
	end=$lines
    fi


    cellprofiler -p outputs$i/Batch_data.h5 -cr -f $start -l $end > outputs$i/log.log 2>&1 &
done

