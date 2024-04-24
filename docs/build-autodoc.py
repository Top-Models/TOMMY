import subprocess
import webbrowser
import os
import shutil

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
