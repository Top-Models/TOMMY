#!/bin/bash

APP_NAME="Tommy"
OUTPUT_FOLDER="dist"
DATA_FOLDER_PATH="tommy/data/preprocessing_data"

echo "> Removing the dist folder if it exists"

rm -r "${OUTPUT_FOLDER}"

echo "> Creating an application bundle for Tommy"

pyinstaller \
--noconfirm \
--windowed \
--onedir \
--name "${APP_NAME}" \
--icon "assets/tommy.svg" \
--add-data "${DATA_FOLDER_PATH}/:./preprocessing_data" \
--hidden-import "pkg_resources.extern" \
tommy/main.py

echo "> You can find the application in the dist folder"
