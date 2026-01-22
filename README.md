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
- Get from “empty directory” to “compiling project” quickly

## Prerequisites

Before using this template, make sure you have:

- **Python 3.7+**
- **Cookiecutter**
- **RBFX engine** (built or downloaded locally)
- **CMake** (3.16 or newer recommended)
- A C++ compiler compatible with C++17

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
  [1/6] project_name (Sample Project): 
  [2/6] project_slug (sample-project): # used for folders and targets
  [3/6] rbfx_sdk (../rbfx): ../rebelfork-sdk-linux-gcc-x64-dll-latest # relative path to the rbfx engine
  [4/6] sample_plugin (y): n # If you want to include and build an example of a plugin
  [5/7] editor (y): n # If you want to include and build an Editor with your game and plugins
  [6/7] min_cmake_version (3.14): 
  [7/7] license (MIT): 
```

After answering the prompts, a new directory containing your project will be created.

## Project Layout (Generated)

A typical generated project looks like this:

```bash
your_project/
├── android
├── CMakeLists.txt
├── Plugins # [OPTIONAL]
│   └── Core.SamplePlugin
│       ├── ...
├── Project
│   ├── Data
│   │   ├── ...
│   └── Project.json
├── ResourceRoot.ini
└── Source
    ├── Application
    │   ├── CMakeLists.txt
    │   ├── SampleProject.cpp
    │   └── SampleProject.h
    ├── Editor # [OPTIONAL]
    │   ├── CMakeLists.txt
    │   └── Editor.cpp
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

Replace ```/path/to/rbfx``` with the location of your RBFX installation or build.

## Running the Application

Once built, run the executable produced in the build directory:

```bash
./your_project
```

On Windows, run the generated .exe file instead.
