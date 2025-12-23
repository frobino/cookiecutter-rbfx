import subprocess
import os

SUBMODULE_REPO = "https://github.com/rbfx/Core.SamplePlugin.git"
SUBMODULE_PATH = "Plugins/Core.SamplePlugin"

def run(cmd):
    subprocess.check_call(cmd, shell=True)

run("git init")
if os.path.isdir(".git"):
    run(f"git submodule add {SUBMODULE_REPO} {SUBMODULE_PATH}")
    run("git submodule update --init --recursive")
else:
    print("Warning: Project is not a Git repository. Skipping submodule setup.")
