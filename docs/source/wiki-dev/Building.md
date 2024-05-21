# Building the Application/Installer

To build the application/installer, a general purpose script can be executed. 
The script can be run by following the steps listed below.

## Prerequisites

- Virtual environment with all dependencies (from requirements.txt) installed and activated
- macOS 10.15 or later / Windows 8 or later / all Linux distributions (although some distribution-specific issues could arise)

## Step 1 - Install PyInstaller

The PyInstaller package is used to generate to build the application and is therefore not included in the requirements.txt file, as it is not a requirement of the application itself. 
Thus, manually install PyInstaller in the virtual environment:
```bash
pip install pyinstaller
```

## Step 1½ - Install create-dmg

The create-dmg script is used to create a disk image (.dmg file) for macOS. 
If you are building on macOS, install the script using your favorite package manager/install script, Homebrew is recommended:
```bash
brew install create-dmg
```

## Step 2 - Execute the Installer Script

Run the `create_installer.py` script that is located in the `installer` directory. 
The working directory in which the script will be executed, should be the root directory of the project. 
The script automatically detects the operating system and executes the appropriate build script:

- On macOS, a disk image file and an app file will be generated in the `dist` directory
- On Windows and Linux, an executable file will be generated in the `dist` directory
