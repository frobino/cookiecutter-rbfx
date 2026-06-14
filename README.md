# cookiecutter-rbfx

[![Weekly Build](https://github.com/frobino/cookiecutter-rbfx/actions/workflows/weekly.yml/badge.svg)](
https://github.com/frobino/cookiecutter-rbfx/actions/workflows/weekly.yml
)

Quickly scaffold a new RBFX game project using Cookiecutter.

This repository provides a Cookiecutter template that generates a ready-to-build **RBFX (C++) game project** with a clean structure.
It is intended for developers who want to start coding immediately without spending time on initial project setup.

> NOTE: tested on Windows and Linux only (no Android yet)

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
  - Windows: Install 7-Zip from https://www.7-zip.org/
- For web build (wasm) you will need:
  - [emscripten](https://emscripten.org/docs/getting_started/downloads.html) installed and configured
  - lz4, e.g. ```apt install python3-lz4```

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
  [2/8] project_slug (sample-project): 
  [3/8] Select sample_plugin
    1 - y
    2 - n
    Choose from [1/2] (1): 
  [4/8] Select editor
    1 - y
    2 - n
    Choose from [1/2] (1): 
  [5/8] min_cmake_version (3.14): 
  [6/8] license (MIT): 
  [7/8] Select rbfx_sdk_install
    1 - dll
    2 - lib
    3 - web
    4 - n
    Choose from [1/2/3/4] (1): 
  [8/8] rbfx_sdk_path (rbfx): 
```

For a complete description of the prompts, see below.

### Prompt Descriptions

Each prompt in the cookiecutter template serves a specific purpose:

**project_name**: Human-readable name for your project (e.g., "My Awesome Game")

**project_slug**: Simple identifier used for both the folder name and CMake project name. Use values like `my-game` or `awesome-project`, not paths. Invalid examples: `C:\Folder\Name`, `/home/user/Name`.

**sample_plugin**: Whether to include and build an example plugin (choose `1` for `y`, `2` for `n`)

**editor**: Whether to include and build a custom Editor target (choose `1` for `y`, `2` for `n`)

**min_cmake_version**: Minimum CMake version required (default: "3.14")

**license**: License for your new project (default: "MIT")

**rbfx_sdk_install**: Whether to download the SDK — choose `1` for `dll` (DLL-based SDK), `2` for `lib` (LIB-based SDK), `3` for `web` (WebAssembly/Emscripten SDK), or `4` for `n` (use an existing SDK).

**rbfx_sdk_path**: Location of the SDK relative to the directory where you are running cookiecutter. This location must contain `bin/CoreData`. If you are letting this template download the SDK (previous prompt), this will be the folder where the SDK will be downloaded. Use values such as `rbfx-SDK` or `../this/folder`, not absolute paths. Invalid examples: `C:\Folder\Name`, `/home/user/Name`

### CLI Usage (non-interactive)

For CI or automated generation, use `--no-input` and set the cookiecutter variables from the command line:

```bash
# Download DLL-based SDK from GitHub releases (URL auto-detected by OS)
cookiecutter . --no-input \
    rbfx_sdk_install="dll" \
    project_name="MyProject" \
    project_slug="my-project"

# Download LIB-based SDK from GitHub releases
cookiecutter . --no-input \
    rbfx_sdk_install="lib" \
    project_name="MyProject" \
    project_slug="my-project"

# Download WebAssembly SDK from GitHub releases
cookiecutter . --no-input \
    rbfx_sdk_install="web" \
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

From inside your generated project directory, the build commands differ depending on whether you chose a DLL-based or LIB-based SDK during project generation.

For DLL-based SDKs (`rbfx_sdk_install="dll"`):

```bash
cmake -DCMAKE_CONFIGURATION_TYPES="Debug" -DBUILD_SHARED_LIBS=ON -DCMAKE_PREFIX_PATH=../rbfx -S . -B ./build && cmake --build build/
```

For LIB-based SDKs (`rbfx_sdk_install="lib"`):

```bash
cmake -DCMAKE_CONFIGURATION_TYPES="Debug" -DBUILD_SHARED_LIBS=OFF -DCMAKE_PREFIX_PATH=../rbfx -S . -B ./build && cmake --build build/
```

For web-based SDKs (`rbfx_sdk_install="web"`):

```bash
# NOTE: the wget command below (and the PACKAGE_TOOL_EXECUTABLE) could be removed if the web sdk contains PackageTool (as the other SDKs) 
wget -O PackageTool.py https://raw.githubusercontent.com/rbfx/rbfx/master/Source/Tools/PackageTool/PackageTool.py
cmake -DWEB=1 -DCMAKE_TOOLCHAIN_FILE=$EMSDK/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake -DCMAKE_PREFIX_PATH=../rbfx -DCMAKE_FIND_ROOT_PATH=../rbfx -DPACKAGE_TOOL_EXECUTABLE="/usr/bin/python3;$(pwd)/PackageTool.py" -S . -B ./build && cmake --build build/
```

Replace `../rbfx` with the location of your RBFX SDK (the same path you specified when generating the project), that must contain `bin/CoreData`.

## Running the Application

Once built, run the executable produced in the build directory:

```bash
cd build/bin
./your_project
```

On Windows, run the generated .exe file instead.

For web builds:

```bash
cd build/bin
python3 -m http.server 8080
```

Then open your browser at ```http://0.0.0.0:8080/``` and click on the html file with the **project_slug** name, e.g. ```sample-project.html```.
