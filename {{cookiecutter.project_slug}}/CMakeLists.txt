cmake_minimum_required(VERSION {{ cookiecutter.min_cmake_version }})
project ({{ cookiecutter.project_slug }})

# C++17 is required for this project.
set (CMAKE_CXX_STANDARD 17)

# Setup output directories.
set (CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set (CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# REBELFORK_SDK logic (adapted from workspace)
set (REBELFORK_SDK "" CACHE STRING "Path to pre-built SDK")
if ("${REBELFORK_SDK}" STREQUAL "")
    add_subdirectory (../rbfx ${CMAKE_BINARY_DIR}/3rdParty/rbfx)
    set (REBELFORK_BIN_DIR "${CMAKE_SOURCE_DIR}/../rbfx/bin")
    set (REBELFORK_CMAKE_DIR "${CMAKE_SOURCE_DIR}/../rbfx/CMake")
else ()
    set (CMAKE_PREFIX_PATH ${REBELFORK_SDK}/share)
    list (APPEND CMAKE_FIND_ROOT_PATH ${REBELFORK_SDK}/share)
    find_package (Urho3D REQUIRED)
    set (REBELFORK_BIN_DIR "${REBELFORK_SDK}/bin")
    set (REBELFORK_CMAKE_DIR "${REBELFORK_SDK}/share/CMake")
endif ()

include (${REBELFORK_CMAKE_DIR}/Modules/UrhoCommon.cmake)

# Include Plugins and application (place your code under Source/)
include_directories (${CMAKE_SOURCE_DIR}/Plugins)
add_subdirectory (${CMAKE_SOURCE_DIR}/Plugins/Core.SamplePlugin)

set (APP_PLUGIN_NAME "App.Main")
set (APP_PLUGIN_LIST "Plugin.Core.SamplePlugin;${APP_PLUGIN_NAME}")

add_subdirectory (${CMAKE_SOURCE_DIR}/Source/Application)
add_subdirectory (${CMAKE_SOURCE_DIR}/Source/Launcher)