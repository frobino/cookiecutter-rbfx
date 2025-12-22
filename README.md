# Cookiecutter template for Sample Project

Generates a project layout matching the repository in this workspace.  
After generation:

- If you answered `yes` to include_rbfx_submodule, run `git submodule update --init --recursive` in the created folder to fetch rbfx and plugin submodules (the original workspace uses [Plugins/Core.SamplePlugin](Plugins/Core.SamplePlugin) and rbfx submodule).

This template includes main CMake scaffolding and a few example source files. Add/copy remaining files (Project/Data, Android, StoreArt, scripts, etc.) into the template folder as needed.