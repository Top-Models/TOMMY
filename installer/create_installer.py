import sys
import os
import subprocess

if __name__ == "__main__":
    access_permissions_command = ['chmod', '+x']
    script_directory = 'installer'
    platform = sys.platform

    match platform:
        case "darwin":
            script = os.path.join(script_directory, 'mac-installer.sh')
            access_permissions_command.append(script)
            subprocess.run(access_permissions_command)
            subprocess.run(script)
        case "linux":
            script = os.path.join(script_directory, 'linux-installer.sh')
            access_permissions_command.append(script)
            subprocess.run(access_permissions_command)
            subprocess.run(script)
        case "win32":
            script = os.path.join(script_directory, 'windows-installer.bat')
            subprocess.run(script)
        case _:
            print("Your OS is not supported!")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
