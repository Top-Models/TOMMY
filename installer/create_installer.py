import sys
import subprocess

if __name__ == "__main__":
    match sys.platform:
        case "darwin":
            subprocess.run('./mac-installer.sh')
        case "win32":
            print("Windows is not supported!")
        case "linux":
            print("Linux is not supported!")
        case _:
            print("Your OS is not supported!")


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
