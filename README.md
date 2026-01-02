# Cookiecutter template for rbfx game

This template includes main CMake scaffolding and a few example source files. Add/copy remaining files (Project/Data, Android, StoreArt, scripts, etc.) into the template folder as needed.

## Generate and build for dll (dynamic)

```
mkdir rbfx-projects && cd rbfx-projects
curl -o rebelfork-sdk-linux-gcc-x64-dll-latest.7z https://github.com/rbfx/rbfx/releases/download/latest/rebelfork-sdk-linux-gcc-x64-dll-latest.7z -L
7za l rebelfork-sdk-linux-gcc-x64-dll-latest.7z
7za x rebelfork-sdk-linux-gcc-x64-dll-latest.7z
cookiecutter <path-to-this-repo> // Specify path to the unzipped ../rebelfork-sdk-linux-gcc-x64-lib-latest
cd sample-project
# NOTE: -DBUILD_SHARED_LIBS=ON needed to force identifying my Linux env as dll
cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_PREFIX_PATH=../rebelfork-sdk-linux-gcc-x64-dll-latest -S . -B ./build
cmake --build ./build
./build/bin/sample-project
```

## Generate and build for lib (static)

TBD
