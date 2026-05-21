#!/usr/bin/env python3

"""
Post-generation hook for cookiecutter-rbfx.

Cookiecutter processes Jinja2 expressions in this file before running it,
so the variable values below are rendered at generation time.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# These variables are populated by Jinja2 during cookiecutter template
# rendering.  They are literal strings after Jinja2 has substituted values.
# ---------------------------------------------------------------------------
_sample_plugin = "{{ cookiecutter.sample_plugin }}"
_rbfx_sdk_install = "{{ cookiecutter.rbfx_sdk_install }}"
_rbfx_sdk_path = "{{ cookiecutter.rbfx_sdk_path }}"
_rbfx_sdk_download_url = "{{ cookiecutter.rbfx_sdk_download_url }}"


_SUBMODULE_REPO = "https://github.com/rbfx/Core.SamplePlugin.git"
_SUBMODULE_PATH = "Plugins/Core.SamplePlugin"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, **kwargs)


def extract_archive(archive_path: Path, dest: Path):
    """Extract .7z archive to dest."""
    exe = shutil.which("7z") or shutil.which("7za")
    if exe:
        run(f'"{exe}" x "{archive_path}" -o"{dest}" -y')
    else:
        print("  Error: 7z/7za required but not found.")
        print("  Install: p7zip-full (Linux), 7zip (macOS), or 7-Zip (Windows).")
        sys.exit(1)


def find_sdk_directory(sdk_parent: Path) -> Path:
    """Locate the actual SDK directory inside sdk_parent.

    RBFX prebuilt releases extract into a folder such as
    ``rebelfork-sdk-linux-gcc-x64-dll-latest``.
    We look for the first subdirectory that contains bin/CoreData.
    """
    for candidate in sdk_parent.iterdir():
        if candidate.is_dir() and (candidate / "bin" / "CoreData").is_dir():
            return candidate
    # Fallback
    for candidate in sdk_parent.iterdir():
        if candidate.is_dir():
            return candidate
    return sdk_parent


def find_sdk_for_cmake(sdk_candidate: Path) -> str:
    """Return a path suitable for -DCMAKE_PREFIX_PATH.

    Searches the candidate and its immediate subdirectories for cmake
    config files (SDKConfig.cmake) or a cmake/rbfx package directory.
    """
    # Check root
    for path in [
        sdk_candidate / "SDKConfig.cmake",
        sdk_candidate / "cmake" / "SDKConfig.cmake",
        sdk_candidate / "lib" / "cmake" / "rbfx",
    ]:
        if path.exists():
            return str(sdk_candidate)

    # Check subdirectories (typical for prebuilt SDKs)
    for subdir in sdk_candidate.iterdir():
        if subdir.is_dir():
            for path in [
                subdir / "SDKConfig.cmake",
                subdir / "cmake" / "SDKConfig.cmake",
                subdir / "lib" / "cmake" / "rbfx",
            ]:
                if path.exists():
                    return str(subdir)
            if (subdir / "include" / "rbfx").exists():
                return str(subdir)

    return str(sdk_candidate)


# ---------------------------------------------------------------------------
# Interactive prompt
# ---------------------------------------------------------------------------

def interactive_sdk_prompt():
    """Show interactive menu for SDK setup.

    Returns:
        (install_method, sdk_path_relative, sdk_url)
    """
    print()
    print("=" * 60)
    print("  RBFX SDK Setup")
    print("=" * 60)
    print()
    print("  Choose how to set up the RBFX engine SDK:")
    print()
    print("  [1] Download prebuilt SDK  (recommended)")
    print("  [2] Use existing SDK       (provide path)")
    print()

    try:
        choice = input("  > ").strip()
    except EOFError:
        print("  Error: no stdin (running non-interactively?).")
        print("  Use: --rbfx_sdk_install=download or --rbfx_sdk_install=existing")
        sys.exit(1)

    if choice in ("1", ""):
        path = input("  SDK location [../rbfx]: ").strip() or "../rbfx"
        print()
        print("  Download source:")
        print()
        print("  [1] GitHub releases (auto-detected for your platform)")
        print("  [2] Custom URL")
        print()
        source = input("  > ").strip() or "1"
        if source == "1":
            plat = sys.platform.lower()
            if plat.startswith("linux"):
                url = "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-dll-latest.7z"
            elif plat == "win32":
                url = "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-windows-x64-dll-latest.7z"
            elif plat == "darwin":
                url = "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-macos-x64-dll-latest.7z"
            else:
                url = "https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-dll-latest.7z"
                print(f"  Warning: unknown platform {plat}, using Linux SDK.")
        else:
            url = input("  Custom URL: ").strip()
        return ("download", path, url)
    else:
        path = input("  SDK path: ").strip()
        if not path:
            print("  Error: SDK path is required.")
            sys.exit(1)
        return ("existing", path, "")


# ---------------------------------------------------------------------------
# Write SDK helper info file
# ---------------------------------------------------------------------------

def _make_info(desc: str, sdk_abs: str, cmake_prefix: str, source: str = None) -> str:
    sep = "=" * 60
    lines = [
        "RBFX SDK Information",
        sep,
        "",
        desc,
        "",
        "Runtime SDK (for CoreData in ResourceRoot.ini):",
        "    " + sdk_abs,
        "",
        "CMake PREFIX_PATH (for -DCMAKE_PREFIX_PATH=):",
        "    " + cmake_prefix,
        "",
    ]
    if source:
        lines.extend(["Downloaded from:", "    " + str(source), ""])
    else:
        lines.append("")
    lines.append("See README.md for build instructions.")
    return "\n".join(lines)


def write_info(project_root: Path, sdk_abs: Path, cmake_prefix: str, desc: str, source: str = None):
    info = project_root / "SDK_INFO.txt"
    info.write_text(_make_info(desc, str(sdk_abs), cmake_prefix, source))


# ---------------------------------------------------------------------------
# Fix ResourceRoot.ini CoreData path
# ---------------------------------------------------------------------------

def fix_resource_root(project_root: Path, sdk_abs: Path):
    """Rewrite CoreData= path in ResourceRoot.ini with actual SDK location."""
    resource_path = project_root / "ResourceRoot.ini"
    if not resource_path.is_file():
        return

    content = resource_path.read_text(encoding="utf-8")
    content = re.sub(
        r"(CoreData\s*=\s*).+?(/bin/CoreData)",
        lambda m: m.group(1) + str(sdk_abs) + m.group(2),
        content,
        flags=re.MULTILINE
    )
    resource_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

# Use the Jinja2-rendered variable names (cleaner for the rest of the code)
sample_plugin = _sample_plugin
rbfx_sdk_install = _rbfx_sdk_install
rbfx_sdk_path = _rbfx_sdk_path
rbfx_sdk_download_url = _rbfx_sdk_download_url

print()
print("=" * 60)
print("  Post-generation hook")
print("=" * 60)
print()

# Decide install method
is_interactive = sys.stdin.isatty()
install_method = None
sdk_rel_path = None
sdk_url = None

if rbfx_sdk_install == "prompt" and is_interactive:
    install_method, sdk_rel_path, sdk_url = interactive_sdk_prompt()
elif rbfx_sdk_install == "download":
    install_method = "download"
    sdk_rel_path = rbfx_sdk_path
    sdk_url = rbfx_sdk_download_url
elif rbfx_sdk_install == "existing":
    install_method = "existing"
    sdk_rel_path = rbfx_sdk_path
    sdk_url = ""
else:
    print(f"  Warning: Unknown rbfx_sdk_install={rbfx_sdk_install!r}. Defaulting to interactive.")
    install_method, sdk_rel_path, sdk_url = interactive_sdk_prompt()

# Resolve paths — cookiecutter runs hooks FROM the project directory,
# so we use cwd() instead of __file__ to find the project root.
project_root = Path.cwd()
sdk_full_path = (project_root.parent / sdk_rel_path).resolve()

# ---------------------------------------------------------------------------
# Download SDK
# ---------------------------------------------------------------------------

if install_method == "download":
    if not sdk_url:
        print("  Error: No download URL provided.")
        print("    Interactive: provide a URL at the prompt.")
        print("    CI/Automated: set rbfx_sdk_download_url or --rbfx_sdk_download_url")
        sys.exit(1)

    print(f"  Downloading SDK to: {sdk_full_path} ...")

    sdk_full_path.parent.mkdir(parents=True, exist_ok=True)

    archive_path = sdk_full_path.parent / "sdk.7z"
    if not archive_path.exists():
        import urllib.request
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
    sdk_dir.rename(sdk_full_path)
    actual_sdk = sdk_full_path

    cmake_prefix = find_sdk_for_cmake(sdk_full_path)

    write_info(project_root, actual_sdk, cmake_prefix,
               "This project was generated with an auto-downloaded SDK.", source=sdk_url)

    print()
    print(f"  SDK downloaded to: {actual_sdk}")
    print(f"  Recommended -DCMAKE_PREFIX_PATH: {cmake_prefix}")
    print()

    # Fix ResourceRoot.ini
    fix_resource_root(project_root, actual_sdk)
    print(f"  Updated ResourceRoot.ini with real SDK path.")
    print(f"  SDK info written to: SDK_INFO.txt")

# ---------------------------------------------------------------------------
# Use existing SDK
# ---------------------------------------------------------------------------

elif install_method == "existing":
    sdk_check = sdk_full_path

    if sdk_check.is_dir() and (sdk_check / "bin" / "CoreData").is_dir():
        cmake_prefix = find_sdk_for_cmake(sdk_check)
        print(f"  Using existing SDK at:   {sdk_check}")
        print(f"  Recommended -DCMAKE_PREFIX_PATH: {cmake_prefix}")
        print()

        write_info(project_root, sdk_check, cmake_prefix, "This project uses an existing SDK.")
        print(f"  SDK info written to: SDK_INFO.txt")
    else:
        print(f"  Error: SDK directory not found at '{sdk_check}'")
        print()
        print("  Ensure the SDK directory contains bin/CoreData")
        print("  Run with: --rbfx_sdk_install=existing --rbfx_sdk_path /path/to/sdk")
        sys.exit(1)

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
