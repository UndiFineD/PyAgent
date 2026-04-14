@echo off
setlocal enabledelayedexpansion
set "ARGS="
:loop
if "%~1"=="" goto done
set "ARG=%~1"
if "%ARG%"=="-3" shift & goto loop
if "%ARG%"=="-2" shift & goto loop
if "%ARG%"=="-" shift & goto loop
if "!ARGS!"=="" (set "ARGS=%~1") else (set "ARGS=!ARGS! %~1")
shift
goto loop
:done
if "!ARGS!"=="" (
    "C:\Dev\PyAgent\.venv\Scripts\python.exe"
) else (
    "C:\Dev\PyAgent\.venv\Scripts\python.exe" !ARGS!
)
