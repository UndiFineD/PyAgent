# Self-Hosted Runner Setup Guide

Complete guide for configuring and troubleshooting the self-hosted GitHub Actions runner.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Service Installation](#service-installation)
- [PATH Configuration](#path-configuration)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)
- [Tool Dependencies](#tool-dependencies)

## Prerequisites

### Required Software

1. **Git for Windows** (required for bash, curl, sha256sum, gpg)
   - Download: <https://git-scm.com/download/win>
   - During installation, ensure "Git from the command line and also from 3rd-party software" is selected
   - Verify installation:

```powershell
where bash
# Should show: C:\Program Files\Git\bin\bash.exe
```

## Service Installation

### Step 1: Obtain Registration Token

1. Navigate to: <https://github.com/UndiFineD/DebVisor/settings/actions/runners>
2. Click "New self-hosted runner"
3. Select "Windows" and "x64"
4. Copy the registration token

### Step 2: Configure Runner

```powershell
cd C:\actions-runner
.\config.cmd --url https://github.com/UndiFineD/DebVisor --token YOUR_TOKEN --runasservice --windowslogonaccount "NT AUTHORITY\SYSTEM"
```

## PATH Configuration

Ensure the runner has access to required tools in PATH.

## Troubleshooting

Common issues and solutions.

## Verification

Verify the runner is working correctly.

## Tool Dependencies

Required tools for the CI/CD pipeline.