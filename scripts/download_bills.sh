#!/bin/bash

START_CONGRESS=110
CURRENT_CONGRESS=116

# Test if ../../congress already exists and terminate with a warning if it does, to avoid overwriting
if [ -d "../../congress" ] 
then 
    echo "Directory ../../congress already exists. This script would overwrite it; you must move or delete it before running this script."
    exit 1
else
    echo "There is no previous directory at ../../congress. Preparing that directory now..."
fi


for CONGRESS in $(seq $START_CONGRESS $CURRENT_CONGRESS)
do
	echo "Downloading data for ${CONGRESS}th Congress"
    curl https://s3.amazonaws.com/pp-projects-static/congress/bills/${CONGRESS}.zip -o ${CONGRESS}.zip

	echo "Unzipping directory for ${CONGRESS}th Congress"
    unzip ${CONGRESS}.zip

    if [ $CONGRESS -eq $START_CONGRESS ]
    then
	    echo "Moving directory for ${CONGRESS}th Congress"
        mv congress/ ../../congress
    else
	    echo "Moving directory for ${CONGRESS}th Congress into existing directory"
        mv congress/data/${CONGRESS}/ ../../congress/data/
    fi
	
    echo "Done downloading and setting up directory. You should have data from ProPublica in ../../congress"

done