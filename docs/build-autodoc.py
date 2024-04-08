import subprocess
import webbrowser
import os

subprocess.run(["sphinx-build", "-M", "html", "docs/source/",
                "docs/build/"])
webbrowser.open('file://' + os.path.abspath('./docs/build/html/index.html'))
