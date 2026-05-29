#!/usr/bin/env python3

"""
Post-generation hook for cookiecutter-rbfx.

Cookiecutter processes Jinja2 expressions in this file before running it,
so the variable values below are rendered into literal strings.
"""

import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Variables populated by Jinja2 during cookiecutter template rendering
# ---------------------------------------------------------------------------
sample_plugin = "{{ cookiecutter.sample_plugin }}"
rbfx_sdk_install = "{{ cookiecutter.rbfx_sdk_install }}"
rbfx_sdk_path = "{{ cookiecutter.rbfx_sdk_path }}"


_SUBMODULE_REPO = "https://github.com/rbfx/Core.SamplePlugin.git"
_SUBMODULE_PATH = "Plugins/Core.SamplePlugin"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: str, **kwargs):
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, **kwargs)


def get_sdk_download_url(buildType: str):
    """Return the appropriate SDK download URL for the current platform."""
    plat = sys.platform.lower()
    if plat.startswith("linux"):
        return "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-" + buildType + "-latest.7z"
    elif plat == "win32":
        # We only support x64 Windows
        return "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-windows-msvc-x64-" + buildType + "-latest.7z"
    else:
        # Fallback to Linux SDK for unknown platforms
        print(f"  Warning: unknown platform {plat}, using Linux SDK built with dll.")
        return "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-dll-latest.7z"


def extract_archive(archive_path: Path, dest: Path):
    exe = shutil.which("7z") or shutil.which("7za")
    if exe:
        run(f'"{exe}" x "{archive_path}" -o"{dest}" -y')
    else:
        print("  Error: 7z/7za required but not found.")
        print("  Install: p7zip-full (Linux), 7zip (macOS), or 7-Zip (Windows).")
        sys.exit(1)


def find_sdk_directory(sdk_parent: Path) -> Path:
    """Locate the actual SDK directory — the first subdir containing bin/CoreData."""
    for candidate in sdk_parent.iterdir():
        if candidate.is_dir() and (candidate / "bin" / "CoreData").is_dir():
            return candidate
    for candidate in sdk_parent.iterdir():
        if candidate.is_dir():
            return candidate
    return sdk_parent


# ---------------------------------------------------------------------------
# Fix ResourceRoot.ini --- Jinja2 renders the template variable but may not
# point to the real extracted SDK location, so we patch it.
# ---------------------------------------------------------------------------

def fix_resource_root(project_root: Path, sdk_abs: Path):
    content_path = project_root / "ResourceRoot.ini"
    if not content_path.is_file():
        return

    # Calculate the relative path from project directory to SDK directory
    try:
        rel_path = os.path.relpath(sdk_abs, project_root)
    except ValueError:
        # This can happen on Windows with different drives
        # Fall back to absolute path
        rel_path = str(sdk_abs)
    
    content = content_path.read_text(encoding="utf-8")
    content = re.sub(
        r"(CoreData\s*=\s*)\.\./.+(/bin/CoreData)",
        lambda m: m.group(1) + rel_path + m.group(2),
        content, flags=re.MULTILINE
    )
    content_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

project_root = Path.cwd()

# Decide install mode
if rbfx_sdk_install == "n":
    install_method, sdk_rel_path = "existing", rbfx_sdk_path
    sdk_url = ""
else:
    install_method, sdk_rel_path = "download", rbfx_sdk_path
    sdk_url = get_sdk_download_url(rbfx_sdk_install)

sdk_full_path = (project_root.parent / sdk_rel_path).resolve()

# ---------------------------------------------------------------------------
# Download SDK
# ---------------------------------------------------------------------------

if install_method == "download":
    if not sdk_url:
        print("  Error: No download URL provided.")
        print("  This is unexpected - the OS detection should have provided a URL.")
        sys.exit(1)

    print(f"  Downloading SDK to: {sdk_full_path} ...")
    sdk_full_path.parent.mkdir(parents=True, exist_ok=True)

    archive_path = sdk_full_path.parent / "sdk.7z"
    if not archive_path.exists():
        print(f"  Downloading from: {sdk_url}")
        urllib.request.urlretrieve(sdk_url, archive_path)
    print(f"  Extracting...")

    sdk_dir = sdk_full_path.parent / "_sdk_extract_tmp"
    if sdk_dir.exists():
        shutil.rmtree(sdk_dir)
    sdk_dir.mkdir(parents=True)
    extract_archive(archive_path, sdk_dir)
    archive_path.unlink()

    actual_sdk = find_sdk_directory(sdk_dir)
    if sdk_full_path.exists():
        shutil.rmtree(sdk_full_path)
    sdk_full_path.mkdir(parents=True)
    # Copy the actual SDK contents directly to the target directory
    # This eliminates the extra directory layer and makes both modes consistent
    for item in actual_sdk.iterdir():
        destination = sdk_full_path / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)

    print(f"  SDK downloaded to: {sdk_full_path}")

    # Patch ResourceRoot.ini so CoreData points to the extracted SDK,
    # not to the default cookiecutter path.
    fix_resource_root(project_root, sdk_full_path)
    print(f"  Updated ResourceRoot.ini with real SDK path.")

# ---------------------------------------------------------------------------
# Use existing SDK
# ---------------------------------------------------------------------------

elif install_method == "existing":
    sdk_check = sdk_full_path

    if not (sdk_check.is_dir() and (sdk_check / "bin" / "CoreData").is_dir()):
        print(f"  Error: SDK directory not found: {sdk_check}")
        print("  Ensure the SDK contains bin/CoreData")
        print("  Or use: --rbfx_sdk_install=y")
        sys.exit(1)

    fix_resource_root(project_root, sdk_check)
    print(f"  Using existing SDK at: {sdk_check}")
    print(f"  Updated ResourceRoot.ini.")

# Copy Data folder from SDK to Project directory
sdk_data_path = sdk_full_path / "bin" / "Data"
project_data_path = project_root / "Project" / "Data"

if sdk_data_path.is_dir():
    print(f"  Copying Data folder from SDK to Project...")
    if project_data_path.exists():
        shutil.rmtree(project_data_path)
    shutil.copytree(sdk_data_path, project_data_path)
    print(f"  Copied Data folder to: {project_data_path}")
else:
    print(f"  Warning: SDK Data folder not found at {sdk_data_path}")

# ---------------------------------------------------------------------------
# Git submodule (sample_plugin)
# ---------------------------------------------------------------------------

if sample_plugin == "y":
    try:
        run("git init")
        if os.path.isdir(".git"):
            run(f'git submodule add {_SUBMODULE_REPO} {_SUBMODULE_PATH}')
            run("git submodule update --init --recursive")
        else:
            print("  Warning: No Git repo. Skipping submodule setup.")
    except subprocess.CalledProcessError:
        print("  Warning: Failed to set up git submodule.")
