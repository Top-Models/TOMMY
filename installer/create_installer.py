import sys
import subprocess

if __name__ == "__main__":
    access_permissions_command = ['chmod', '+x', 'installer/mac-installer.sh']
    platform = sys.platform
    script = ''

    match platform:
        case "darwin":
            script = 'installer/mac-installer.sh'
        case "win32":
            script = 'installer/linux-installer.sh'
            #script = 'installer/windows-installer.bat'
        case "linux":
            script = 'installer/linux-installer.sh'
        case _:
            print("Your OS is not supported!")

    # Give access permissions and run the installer script
    if platform in ["darwin", "win32", "linux"]:
        access_permissions_command.append(script)
        subprocess.run(access_permissions_command)
        subprocess.run(script)


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
