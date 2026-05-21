# cookiecutter-rbfx

[![Weekly Build](https://github.com/frobino/cookiecutter-rbfx/actions/workflows/weekly.yml/badge.svg)](
https://github.com/frobino/cookiecutter-rbfx/actions/workflows/weekly.yml
)

Quickly scaffold a new RBFX game project using Cookiecutter.

This repository provides a Cookiecutter template that generates a ready-to-build **RBFX (C++) game project** with a clean structure.
It is intended for developers who want to start coding immediately without spending time on initial project setup.

> NOTE: tested on Windows and Linux only (no Android or web yet)

## What This Is For

Use this template if you want to:

- Start a new **RBFX game or application**
- Avoid manually setting up CMake, folders, and boilerplate files
- Follow a consistent and repeatable project structure
- Get from "empty directory" to "compiling project" quickly

## Prerequisites

Before using this template, make sure you have:

- **Python 3.7+**
- **Cookiecutter**
- **CMake** (3.16 or newer recommended)
- A C++ compiler compatible with C++17
- **7z/7za** (for downloading prebuilt SDKs — see below)
  - Linux: `sudo apt-get install p7zip-full`
  - macOS: `brew install p7zip`
  - Windows: Install 7-Zip from https://www.7-zip.org/

Install Cookiecutter if needed:

```bash
pip install cookiecutter
```

## Creating a New Project

Generate a new RBFX project by running:

```bash
cookiecutter https://github.com/frobino/cookiecutter-rbfx.git
```

You will be prompted for a few values:

```bash
  [1/7] project_name (Sample Project): 
  [2/7] project_slug (sample-project): # used for folders and targets
  [3/7] rbfx_sdk_install (existing):   # ↓ 1. download  2. existing
  [4/7] rbfx_sdk_path (../rbfx):       # SDK save location
  [5/7] rbfx_sdk_download_url ():      # auto-detected per-platform (download mode)
  [6/7] sample_plugin (y): n          # If you want to include and build an example of a plugin
  [7/7] editor (y): n                 # If you want to include and build a custom Editor target
```

For a complete description of the prompts, see below.

### SDK Setup Flow

When you run the template, you will first choose how to obtain the RBFX engine SDK:

**[1] Download prebuilt SDK** (recommended)
- The template downloads the matching prebuilt SDK for your platform.
- After answering the SDK install prompt, you will be asked to confirm the SDK save location (default: `../rbfx` sibling to your project).
- Then you can choose to download from GitHub releases (default, auto-detected for Linux/Windows/macOS) or provide a custom URL.
- The downloaded SDK is extracted and placed in the chosen location.

**[2] Existing SDK** (advanced)
- Use this if you have already built or downloaded an SDK.
- You will be asked for the absolute or relative path to the SDK directory.
- The hook verifies the SDK exists and contains `bin/CoreData`.

### CLI Usage (non-interactive)

For CI or automated generation, use `--no-input` and set the cookiecutter variables from the command line:

```bash
# Download SDK from GitHub releases
cookiecutter . --no-input \
    rbfx_sdk_install=download \
    rbfx_sdk_download_url="https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-dll-latest.7z" \
    project_name="MyProject" \
    project_slug="my-project"

# Use existing SDK
cookiecutter . --no-input \
    rbfx_sdk_install=existing \
    rbfx_sdk_path="/absolute/path/to/sdk" \
    project_name="MyProject" \
    project_slug="my-project"
```

After answering the prompts, a new directory containing your project will be created.

## Project Layout (Generated)

A typical generated project looks like this:

```bash
your_project/
├── android
├── CMakeLists.txt
├── Plugins # [OPTIONAL]
│   └── Core.SamplePlugin
│       ├── ...
├── Project
│   ├── Data
│   │   ├── ...
│   └── Project.json
├── ResourceRoot.ini
└── Source
    ├── Application
    │   ├── CMakeLists.txt
    │   ├── SampleProject.cpp
    │   └── SampleProject.h
    ├── Editor # [OPTIONAL]
    │   ├── CMakeLists.txt
    │   └── Editor.cpp
    └── Launcher
        ├── CMakeLists.txt
        └── Launcher.cpp
```

This layout follows common RBFX and CMake conventions and is ready to build.

## Building the Project

From inside your generated project directory:

```bash
mkdir build
cd build
cmake .. -DCMAKE_PREFIX_PATH=/path/to/rbfx
cmake --build .
```

Replace `/path/to/rbfx` with the location of your RBFX SDK (the same path you specified when generating the project).

## Running the Application

Once built, run the executable produced in the build directory:

```bash
./your_project
```

On Windows, run the generated .exe file instead.
