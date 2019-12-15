#!/usr/bin/bash

file_num=$(ls -1 | egrep -o "result[[:digit:]]" | wc -l)
touch result.csv
for (( i=0; i<$file_num; i++ ))
do
   current_file="result${i}.csv"
   cat "$current_file" >> result.csv
   rm "$current_file"
done
