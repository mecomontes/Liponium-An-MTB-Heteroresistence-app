#!/bin/bash

# Download the reads using Fasterq-dump
echo "Download the .fastq files from SRA usin the liste files in $1";

for i in $(cat $1.txt); do
    echo "Downloading $i...";
    fasterq-dump -Spe 16 $i;
    done

mkdir $1 && mv *fastq $1 && pigz "$1"/*fastq
echo "Finishing Cluster"

