import subprocess
import webbrowser
import os
import shutil


if __name__ == "__main__":
    # Define paths
    autosummary_path = os.path.join('docs', 'source', '_autosummary')
    build_path = os.path.join('docs', 'build')

    # Delete previous build
    def delete_directory(path):
        if os.path.exists(path):
            print(f"Deleting {path}")
            shutil.rmtree(path)


    delete_directory(autosummary_path)
    delete_directory(build_path)

    subprocess.run(["sphinx-build", "-M", "html", "docs/source/",
                    "docs/build/"])
    webbrowser.open('file://' + os.path.abspath('./docs/build/html/index.html'))

"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""
