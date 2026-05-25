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
  [1/8] project_name (Sample Project): 
  [2/8] project_slug (sample-project): # project folder location (relative to parent directory)
  [3/8] sample_plugin (y):             # If you want to include and build an example of a plugin
  [4/8] editor (y):                    # If you want to include and build a custom Editor target
  [5/8] min_cmake_version (3.14):      # If you need specific CMake version
  [6/8] license (MIT):                 # License for your new project
  [7/8] rbfx_sdk_install (y):          # y = download SDK, n = do not download SDK
  [8/8] rbfx_sdk_path (rbfx):          # SDK location (relative to parent directory)
```

For a complete description of the prompts, see below.

### SDK Setup

When you run the template, you will specify whether to download the RBFX engine SDK:

**rbfx_sdk_install = y** (recommended)
- The template automatically detects your operating system and downloads the matching prebuilt SDK from GitHub.
- Supported platforms: Linux, Windows, and macOS.
- The SDK contents will be extracted directly to the directory specified in `rbfx_sdk_path` (default: `rbfx`).
- The project will reference the SDK using a relative path.

**rbfx_sdk_install = n** (advanced)
- You must have already downloaded and extracted the SDK to the directory specified in `rbfx_sdk_path`.
- The directory must contain the `bin/CoreData` folder.
- The project will reference the SDK using a relative path.

### CLI Usage (non-interactive)

For CI or automated generation, use `--no-input` and set the cookiecutter variables from the command line:

```bash
# Download SDK from GitHub releases (URL auto-detected by OS)
cookiecutter . --no-input \
    rbfx_sdk_install=y \
    project_name="MyProject" \
    project_slug="my-project"

# Use existing SDK
cookiecutter . --no-input \
    rbfx_sdk_install=n \
    rbfx_sdk_path="my-custom-sdk" \
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
