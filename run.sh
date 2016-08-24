#!/bin/bash
#set -x
#echo on

CONFIG=dataselection.txt
while read i; 
do 
   OLDIFS=$IFS
   IFS=$'\t'
   a=( $i )
   NAME=${a[0]}
   DATASET_ID_STR=${a[1]}
   PORT=${a[2]}
   #output data id strings to dataselection
   echo "echo $DATASET_ID_STR > dataimportselection.txt"
   echo $DATASET_ID_STR > dataimportselection.txt

   #run docker build and docker run
   echo docker build -t wesc:${NAME} .
   docker build -t wesc:${NAME}  .
   echo docker run -d -p ${PORT}:443 -P wesc:${NAME}
   docker run -d -p ${PORT}:443 -P wesc:${NAME}
   echo
done < $CONFIG
IFS=$OLDIFS
