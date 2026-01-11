# Installation Guide: llama.cpp

This guide describes how to install and use llama.cpp, a port of Facebook's LLaMA model in C/C++ for efficient local inference.

## Prerequisites

- [Git](https://git-scm.com/)
- A C++ compiler (GCC, Clang, or MSVC)
- [CMake](https://cmake.org/) (recommended)
- Large Language Models in GGUF format

## Installation

### macOS / Linux (using Make)
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```

### Windows (using CMake/MSVC)
1. Install [Visual Studio](https://visualstudio.microsoft.com/vs/community/) with "Desktop development with C++".
2. Open a developer command prompt.
3. Run:
```cmd
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

## Configuration

Download a model in `.gguf` format (e.g., from Hugging Face) and place it in the `models/` directory inside the `llama.cpp` folder.

## Basic Usage

### Run Text Generation
```bash
./main -m models/llama-2-7b-chat.Q4_K_M.gguf -p "What is the capital of France?" -n 128
```

### Interactive Mode
```bash
./main -m models/llama-2-7b-chat.Q4_K_M.gguf -i -ins
```

## Documentation
For more details, visit the [llama.cpp GitHub repository](https://github.com/ggerganov/llama.cpp).
