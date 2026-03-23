# Project Overview: prj0000050 — Install Script

## Project Identity

**Project ID:** prj0000050  
**Short name:** install-script  
**Project folder:** `docs/project/prj0000050/`  
**Status:** In Progress  
**Created:** 2026-03-23  

## Project Overview

Developer setup automation for PyAgent on Windows. Provides `install.ps1` at the repository root so a new contributor can clone the repo and run a single script to get a fully working development environment.

## Goal & Scope

**Goal:** Create `install.ps1` — a PowerShell script that automates the full developer setup for PyAgent on Windows, including Python virtual environment creation, pip dependency installation, Rust toolchain verification, and Node.js/npm dependency installation.

**In scope:**
- Create `install.ps1` at repo root with `[CmdletBinding()]`, param block, comment-based help, and phased setup functions
- Structure tests in `tests/structure/test_install_script.py`
- Exec validation doc in `docs/project/prj0000050/install-script.exec.md`
- Optional: update `README.md` to reference the install script

**Out of scope:**
- Modifying application source code
- Modifying CI workflows
- Cross-platform (Linux/macOS) support

## Branch Plan

**Expected branch:** `prj0000050-install-script`  
**Base:** `main`  
**Scope boundary:** Only `install.ps1`, test files, and docs under `docs/project/prj0000050/` will be added or modified.  
**Handoff rule:** Each agent validates their phase before handing off; blockers are documented immediately.  
**Failure rule:** If a setup step cannot be automated (e.g. requires interactive GUI installer), it is documented as a manual step in the script's output rather than silently skipped.

## Lessons Learned

(to be filled by @9git after completion)
