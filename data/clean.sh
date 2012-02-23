#!/bin/bash

for f in $(ls ./scraped_decks/); do
	fname="./scraped_decks/$f"
	#echo $fname
	cat $fname | grep "<|>" > /dev/null
	if [ $? -ne 0 ]; then
		echo "deleting $fname"
		rm $fname
	fi
done
