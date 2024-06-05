@echo off

set APP_NAME=Tommy
set OUTPUT_FOLDER=dist
set DATA_FOLDER_PATH=tommy/data/preprocessing_data

echo ^> Removing the dist folder if it exists

if exist %OUTPUT_FOLDER% (
    rmdir /s /q %OUTPUT_FOLDER%
)

echo ^> Creating an application bundle for Tommy

pyinstaller ^
--noconfirm ^
--windowed ^
--onedir ^
--name "%APP_NAME%" ^
--name "%APP_NAME%" ^
--icon "assets/tommy.ico" ^
--add-data "%DATA_FOLDER_PATH%:.\preprocessing_data" ^
--hidden-import "pkg_resources.extern" ^
tommy/main.py

echo ^> You can find the application in the dist folder
