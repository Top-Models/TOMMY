#!/bin/zsh

echo "> Creating an application bundle for Tommy"

pyinstaller \
--noconfirm \
--windowed \
--onedir \
--name "Tommy" \
--icon "assets/tommyBackground.icns" \
--add-data "tommy/data/csv_files/*.csv:./data" \
--add-data "tommy/data/stopwords.txt:./preprocessing_data" \
--add-data "tommy/data/pipeline_download:./preprocessing_data/pipeline_download" \
tommy/main.py

echo "> Creating a DMG file for Tommy"

create-dmg \
--volname "Tommy" \
--volicon "assets/tommyBackground.icns" \
--background "assets/installerBackground.png" \
--window-pos 200 120 \
--window-size 835 600 \
--icon-size 128 \
--icon "Tommy.app" 230 250 \
--hide-extension "Tommy.app" \
--app-drop-link 593 250 \
--no-internet-enable \
"dist/Tommy.dmg" \
"dist/Tommy.app"

echo "> You can find the DMG file in the dist folder"
