# Cookiecutter template for rbfx game

Generates a project layout matching the repository in this workspace.  
After generation:

- If you answered `yes` to include_rbfx_submodule, run `git submodule update --init --recursive` in the created folder to fetch rbfx and plugin submodules (the original workspace uses [Plugins/Core.SamplePlugin](Plugins/Core.SamplePlugin) and rbfx submodule).

This template includes main CMake scaffolding and a few example source files. Add/copy remaining files (Project/Data, Android, StoreArt, scripts, etc.) into the template folder as needed.

## How to

```
curl -o test.7z https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-lib-latest.7z -L
7za l test.7z
7za x test.7z
cookiecutter ... // Specify path to the unzipped rebelfork-sdk-linux-gcc-x64-lib-latest
cd sample-project
cmake -DCMAKE_PREFIX_PATH=../rebelfork-sdk-linux-gcc-x64-lib-latest -S . -B ./build
cmake --build ./build
./build/bin/sample-project
```

## Next

- fix include_rbfx_submodule
