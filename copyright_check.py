import os


utrecht_license = """
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""


def check_licence(path: str) -> bool:
    """
    Check if a file has the Utrecht University license.
    :param path: The path to check
    :return: False if missing license
    """

    if path.endswith(".py"):
        with open(path, "r") as f:
            return utrecht_license in f.read()

    return True  # non-python always valid


if __name__ == "__main__":
    # Get all files in the working directory
    current_path = os.path.dirname(os.path.realpath(__file__))
    files = os.walk(current_path)

    ignore = [".git", "venv", "dist", "build"]

    for ignore_directory in ignore:
        ignore_path = os.path.join(current_path, ignore_directory)
        files = [f for f in files if ignore_path not in f[0]]

    print(f"Searching for .py files missing license in {current_path}")

    for root, dirs, files in files:
        for file in files:
            if not check_licence(str(os.path.join(root, file))):
                print(f'{os.path.join(root, file)[len(current_path):]}')

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
