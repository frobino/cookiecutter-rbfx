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
  [2/8] project_slug (sample-project): # project identifier (used for folder name and CMake project name)
  [3/8] sample_plugin (y):             # If you want to include and build an example of a plugin
  [4/8] editor (y):                    # If you want to include and build a custom Editor target
  [5/8] min_cmake_version (3.14):      # If you need specific CMake version
  [6/8] license (MIT):                 # License for your new project
  [7/8] rbfx_sdk_install (y):          # y = download SDK, n = do not download SDK
  [8/8] rbfx_sdk_path (rbfx):          # SDK location (relative to directory where cookiecutter is executed)
```

For a complete description of the prompts, see below.

### Prompt Descriptions

Each prompt in the cookiecutter template serves a specific purpose:

**project_name**: Human-readable name for your project (e.g., "My Awesome Game")

**project_slug**: Simple identifier used for both the folder name and CMake project name. Use values like `my-game` or `awesome-project`, not paths. Invalid examples: `C:\Folder\Name`, `/home/user/Name`.

**sample_plugin**: Whether to include and build an example plugin (`y` or `n`)

**editor**: Whether to include and build a custom Editor target (`y` or `n`)

**min_cmake_version**: Minimum CMake version required (default: "3.14")

**license**: License for your new project (default: "MIT")

**rbfx_sdk_install**: Whether to download the SDK (`y`) or use an existing one (`n`)

**rbfx_sdk_path**: Location of the SDK relative to the directory where you are running cookiecutter. This location must contain `bin/CoreData`. If you are letting this template download the SDK (previous prompt), this will be the folder where the SDK will be downloaded. Use values such as `rbfx-SDK` or `../this/folder`, not absolute paths. Invalid examples: `C:\Folder\Name`, `/home/user/Name`

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
<project_slug>/
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

Replace `/path/to/rbfx` with the location of your RBFX SDK (the same path you specified when generating the project), that must contain `bin/CoreData`.

Note that the exact command can be different depening on the version of the SDK (dll, lib, etc.).

## Running the Application

Once built, run the executable produced in the build directory:

```bash
./your_project
```

On Windows, run the generated .exe file instead.
