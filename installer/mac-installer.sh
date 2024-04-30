#!/bin/bash

APP_NAME="Tommy"
VOLUME_NAME="${APP_NAME} Installer"
OUTPUT_FOLDER="dist"
DMG_FOLDER_PATH="${OUTPUT_FOLDER}/${APP_NAME}-Installer.dmg"
SOURCE_FOLDER_PATH="${OUTPUT_FOLDER}/${APP_NAME}.app"
DATA_FOLDER_PATH="tommy/data"

echo "> Removing the dist folder if it exists"

rm -r "${OUTPUT_FOLDER}"

echo "> Creating an application bundle for Tommy"

pyinstaller \
--noconfirm \
--windowed \
--onedir \
--name "${APP_NAME}" \
--icon "assets/tommyBackground.icns" \
--add-data "${DATA_FOLDER_PATH}/csv_files/*.csv:./data" \
--add-data "${DATA_FOLDER_PATH}/stopwords.txt:./preprocessing_data" \
--add-data "${DATA_FOLDER_PATH}/pipeline_download:./preprocessing_data/pipeline_download" \
tommy/main.py

echo "> Creating a DMG file for Tommy"

create-dmg \
--volname "${VOLUME_NAME}" \
--volicon "assets/tommyBackground.icns" \
--background "assets/img.png" \
--window-pos 200 120 \
--window-size 800 600 \
--icon-size 128 \
--icon "${APP_NAME}.app" 230 250 \
--hide-extension "${APP_NAME}.app" \
--app-drop-link 593 250 \
--no-internet-enable \
"${DMG_FOLDER_PATH}" \
"${SOURCE_FOLDER_PATH}"

echo "> You can find the DMG file in the dist folder"
