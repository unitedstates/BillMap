#!/bin/bash

START_CONGRESS=110
CURRENT_CONGRESS=116
CONGRESS_SEQ=$(seq $CURRENT_CONGRESS -1 $START_CONGRESS)

LOCAL_TMP=tmp
TARGET_CONGRESS_DIR=../../congress

if [ -d "${LOCAL_TMP}" ] 
then
    echo "${LOCAL_TMP}/ found"
else
    echo "Creating ${LOCAL_TMP}/ for downloads"
    mkdir "${LOCAL_TMP}"
fi

echo "Downloading data for Congresses: ${CONGRESS_SEQ}"

for CONGRESS in $CONGRESS_SEQ 
do
    if [ -f "${LOCAL_TMP}/${CONGRESS}.zip" ] 
    then
        echo "${LOCAL_TMP}/${CONGRESS}.zip already exists. Skipping...". 
    else
        echo "Downloading data for ${CONGRESS}th Congress to ${LOCAL_TMP}/${CONGRESS}.zip"
        curl https://s3.amazonaws.com/pp-projects-static/congress/bills/${CONGRESS}.zip -o ${LOCAL_TMP}/${CONGRESS}.zip

        echo "Done downloading data for ${CONGRESS} to ${LOCAL_TMP}/${CONGRESS}.zip". 
    fi

done

for CONGRESS in $CONGRESS_SEQ 
do
	echo "Unzipping directory for ${CONGRESS}th Congress"
    unzip "${LOCAL_TMP}/${CONGRESS}.zip"  -x "__MACOSX/*" -d "${LOCAL_TMP}/${CONGRESS}/"
    echo "Done unpacking data from ${CONGRESS}. You can now find it in ${LOCAL_TMP}/${CONGRESS}"
	
done

# Test if $TARGET_CONGRESS_DIR already exists and terminate with a warning if it does, to avoid overwriting
if [ -d "${TARGET_CONGRESS_DIR}" ] 
then 
    echo "Directory ${TARGET_CONGRESS_DIR} already exists. This script would overwrite it; you must move or delete it before running this script."
    exit 1
else
    echo "There is no previous directory at ${TARGET_CONGRESS_DIR}. Preparing that directory now..."
    mkdir -p ${TARGET_CONGRESS_DIR}/data
    mkdir -p ${TARGET_CONGRESS_DIR}/data/relatedbills

    # Handle directories that open to $CONGRESS (e.g. 115/) instead of congress/
    for CONGRESS in $CONGRESS_SEQ
    do
        if [ -d "${LOCAL_TMP}/${CONGRESS}/congress/data/${CONGRESS}" ] 
        then
            mv "${LOCAL_TMP}/${CONGRESS}/congress/data/${CONGRESS}" "${TARGET_CONGRESS_DIR}/data/${CONGRESS}"
        fi

        if [ -d "${LOCAL_TMP}/${CONGRESS}/${CONGRESS}" ] 
        then
            mv "./${LOCAL_TMP}/${CONGRESS}/${CONGRESS}" "${TARGET_CONGRESS_DIR}/data/${CONGRESS}"
        fi

        if [ -d "${LOCAL_TMP}/${CONGRESS}/bills" ] 
        then
            mkdir "${TARGET_CONGRESS_DIR}/data/${CONGRESS}" 
            mv "./${LOCAL_TMP}/${CONGRESS}/bills" "${TARGET_CONGRESS_DIR}/data/${CONGRESS}/"
        fi
    done
    echo "Done. Data is now available in ${TARGET_CONGRESS_DIR}."
    # TODO: check that directories have been made, then remove tmp
    # rm -r ${LOCAL_TMP}
fi