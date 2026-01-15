# Rust Installation Guide for PyAgent

This guide covers the installation of Rust and the necessary build tools to compile the `rust_core` native extension for PyAgent.

## Prerequisites

- **Python 3.10+** (Already installed for PyAgent)
- **Windows 10/11**
- **Git**

## 1. Install Rust via Rustup

The recommended way to install Rust is via `rustup`.

1.  Download `rustup-init.exe` from [rust-lang.org](https://rust-lang.org/tools/install).
2.  Run the installer.
3.  When prompted, choose the default installation (type `1` and press Enter).
4.  Restart your terminal (PowerShell or Command Prompt).
5.  Verify the installation:
    ```powershell
    rustc --version
    cargo --version
    ```

## 2. Install Build Tools (Windows)

Rust on Windows requires the **C++ Build Tools** from Visual Studio.

1.  Download and install [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2.  In the installer, select the **Desktop development with C++** workload.
3.  Ensure the following components are checked:
    -   MSVC v143 - VS 2022 C++ x64/x86 build tools
    -   Windows 10/11 SDK (e.g., 10.0.19041.0)
4.  Restart your computer if prompted.

## 3. Install Maturin

`maturin` is the build system used to bridge Rust and Python.

With your PyAgent virtual environment activated:
```powershell
pip install maturin
```

## 4. Compiling rust_core

To compile the Rust extension for development:

1.  Navigate to the project root:
    ```powershell
    cd C:\DEV\PyAgent
    ```
2.  Run maturin develop:
    ```powershell
    maturin develop
    ```

> **Note for Windows Users:** If you encounter linker errors regarding `kernel32.lib`, ensure you run `vcvars64.bat` in your terminal session or use the x64 Native Tools Command Prompt for VS 2022.

## 5. Troubleshooting

### Linker Error: `kernel32.lib` not found
This usually means the Windows SDK is missing or the environment variables are not set.
-   Verify the Windows SDK is installed via the Visual Studio Installer.
-   Run the following in PowerShell before building:
    ```powershell
    & "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    ```

### PyO3 Compilation Errors
Ensure you are using the latest version of `maturin` and that your `Cargo.toml` specifies the correct `pyo3` features (usually `extension-module`).
