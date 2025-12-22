# This hook runs after cookiecutter generation.
import os
import subprocess
from pathlib import Path

project_dir = Path(os.getcwd())

def run(cmd):
    try:
        subprocess.check_call(cmd, shell=True, cwd=project_dir)
    except subprocess.CalledProcessError:
        print("Command failed:", cmd)

# If template asked to include rbfx submodule, initialize submodules.
if "{{ cookiecutter.include_rbfx_submodule }}" == "yes":
    print("Initializing git submodules (rbfx, Plugins)...")
    run("git submodule update --init --recursive")