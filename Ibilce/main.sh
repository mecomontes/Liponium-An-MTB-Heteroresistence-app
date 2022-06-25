#!/bin/bash

echo "Download the .fastq files from SRA";

for i in {5..7}; do
    echo "Create cluster $i...";
    if [[ $i -lt 10 ]]
    then
        sh ./download_reads.sh $10$i;
    else
    	sh ./download_reads.sh $1$i;
    fi
done

echo "Downoad finished!"

