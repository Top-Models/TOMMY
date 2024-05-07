# Generating a Disk Image for macOS

## Prerequisites

- macOS 10.15 or later
- Virtual environment with all dependencies (from requirements.txt) installed and activated

## Step 1 - Install PyInstaller

The PyInstaller package is used to generate an application and is not included in the requirements.txt file, as it is not a requirement of the application itself. 
Therefore, manually install PyInstaller in the virtual environment:
```bash
pip install pyinstaller
```

## Step 2 - Install create-dmg

The create-dmg script is used to create a disk image (.dmg file) for macOS. 
Install the script using your favorite package manager/install script, Homebrew is recommended:
```bash
brew install create-dmg
```

## Step 3 - Generate the Disk Image w/ the Application

Navigate to the root directory of the project and activate the virtual environment. 
Once the virtual environment is activated, run the following command to change file permissions for the installer script (this only has to be done once):
```bash
chmod +x installer/mac-installer.sh
```

Next, run the installer script to generate the disk image:
```bash
installer/mac-installer.sh
```

The disk image will be generated in the `dist` directory of the project's root directory.