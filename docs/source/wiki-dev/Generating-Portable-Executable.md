# Generating Executable with PyInstaller

## Prerequisites

- You need to have the virtual environment installed and activated (for help, see the "venv setup guide" in Documents/General/Styleguides and Tutorials in our Sharepoint or ask Wessel, @2828189 )

## Step 1 - Install PyInstaller

PyInstaller is not included in the requirements.txt in our project, because it is not a requirement of our application itself. Therefore we need to install it manually in our virtual environment. In a terminal where the venv is activated install it using pip (this venv is automatically active in the terminal inside pycharm), run the command:

`pip install pyinstaller` or `pip3 install pyinstaller`

## Step 2 - Generate Executable

We can generate the installer with one command inside the same terminal:

`pyinstaller --noconsole --onedir tommy/main.py`

Now pyinstaller should generate a "build" folder, which we can ignore, and a "dist/main" folder, which contains the executable and an "\_internal" folder containing the modules and other data.

## Adding data to the build directory

We might need to add more data to the build directory. For example the stopwords.txt will be expected in some path relative to the working directory. To do this we add another build option to the command like this: `--add-data "tommy/stopwords.txt:./my_relative_destination_folder"`. See [add-data](https://pyinstaller.org/en/stable/usage.html#cmdoption-add-data)

To make our executable work we need the downloaded spacy pipeline and the stopwords file (the input data can be selected from within the application, so there is no real need to copy those). So an entire command that should work on main right now would be:

`pyinstaller --noconsole --onedir --add-data "tommy/data/stopwords.txt:./preprocessing_data/" --add-data "tommy/data/pipeline_download/:./preprocessing_data/pipeline_download" tommy/main.py`

The program should now run correctly on all the csv files in the `data` folder when executing `dist/main/main.exe`

### Notes

- `tommy/main.py` in the command above should be the path from the current location of the terminal to main.
- After running this command, `main.spec` is created, which saves the build settings. So you can build it again with the same options by running `pyinstaller main.spec`
- We use the --onedir option instead of --onefile because:
  - On macOS, when using --onefile (singe executable), the current directory is listed as C:/user/\[name_of_user\] instead of the location of the executable.
  - When using --onefile, the program creates a "\_MEI\[number\]" folder in your temporary appdata folder everytime the program is ran (which is deleted afterwards). This makes the startup slower than the --onedir option.