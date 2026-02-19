# /// script
# dependencies = ["sphinx-autobuild", "sphinx", "furo", "myst-parser"]
# ///
import subprocess
import sys

sys.exit(subprocess.call(["sphinx-autobuild", "docs/source", "docs/build/html"]))
