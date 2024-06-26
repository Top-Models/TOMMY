#!/bin/bash

APP_NAME="TOMMY"
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
--icon "${DATA_FOLDER_PATH}/assets/tommy.svg" \
--add-data "${DATA_FOLDER_PATH}/:./data" \
--hidden-import "pkg_resources.extern" \
--exclude tkinter --exclude _tkinter \
--exclude-module torch \
tommy/main.py

echo "> You can find the application in the dist folder"
