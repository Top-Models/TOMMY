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
--icon "assets/tommy.icns" \
--add-data "${DATA_FOLDER_PATH}/stopwords.txt:./preprocessing_data" \
--add-data "${DATA_FOLDER_PATH}/pipeline_download:./preprocessing_data/pipeline_download" \
tommy/main.py

echo "> Creating a DMG file for Tommy"

create-dmg \
--volname "${VOLUME_NAME}" \
--volicon "assets/tommy.icns" \
--background "assets/installerBackground.png" \
--window-pos 200 120 \
--window-size 835 680 \
--icon-size 128 \
--icon "${APP_NAME}.app" 220 285 \
--hide-extension "${APP_NAME}.app" \
--app-drop-link 603 285 \
--no-internet-enable \
"${DMG_FOLDER_PATH}" \
"${SOURCE_FOLDER_PATH}"

echo "> Signing the DMG file"

# TODO: Fix the signing (maybe only necessary for the dmg file?)
#codesign --force --verbose  --verify--timestamp --sign "Developer ID Application: TTT" "${DMG_FOLDER_PATH}"

echo "> You can find the DMG file in the dist folder"
