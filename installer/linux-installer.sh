#!/bin/bash

APP_NAME="Tommy"
OUTPUT_FOLDER="dist"
DATA_FOLDER_PATH="tommy/data"

echo "> Removing the dist folder if it exists"

rm -r "${OUTPUT_FOLDER}"

echo "> Creating an application bundle for Tommy"

pyinstaller \
--noconfirm \
--windowed \
--onedir \
--name "${APP_NAME}" \
--icon "assets/tommy.svg" \
--add-data "${DATA_FOLDER_PATH}/stopwords.txt:./preprocessing_data" \
--add-data "${DATA_FOLDER_PATH}/pipeline_download:./preprocessing_data/pipeline_download" \
tommy/main.py

echo "> You can find the application in the dist folder"
