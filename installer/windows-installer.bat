@echo off

:: Due to problems with numpy (probably because of bertopic)
:: the windows executable cannot be generated by this file
:: but only using this command directly in a terminal:
:: pyinstaller --noconfirm --windowed --onedir --name "Tommy" --icon "assets/tommy.ico" --hidden-import "pkg_resources.extern" --add-data "tommy/data/preprocessing_data/:./preprocessing_data/" tommy/main.py

set APP_NAME=TOMMY
set OUTPUT_FOLDER=dist
set DATA_FOLDER_PATH=tommy/data

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
--icon "assets/tommy.ico" ^
--add-data "%DATA_FOLDER_PATH%:.\data" ^
--hidden-import "pkg_resources.extern" ^
--exclude-module torch ^
tommy/main.py

echo ^> You can find the application in the dist folder
