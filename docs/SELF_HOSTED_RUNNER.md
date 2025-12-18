# Self-Hosted GitHub Actions Runner Setup

## Overview

This repository uses a self-hosted GitHub Actions runner to execute CI/CD
workflows on local infrastructure. This provides better control over
resources, permissions, and access to local services.

## Benefits

- **Permissions**: Full control over repository and workflow permissions
- **Resources**: Use your own hardware specifications
- **Local Access**: Test against local Ceph clusters, VMs, networks
- **Cost**: No GitHub Actions minutes consumed
- **Customization**: Install any tools, dependencies, or services needed

## Prerequisites

- Windows 10/11 or Windows Server 2019+
- PowerShell 5.1 or later
- Administrator access (for service installation)
- Network access to GitHub (<https://github.com>)

## Installation Steps

### 1. Download and Extract Runner

```powershell
# Create runner directory
mkdir C:\actions-runner
cd C:\actions-runner

# Download latest runner package
Invoke-WebRequest -Uri `
  <https://github.com/actions/runner/releases/download/v2.329.0/ `
  `actions-runner-win-x64-2.329.0.zip> `
  -OutFile actions-runner.zip

# Extract the runner
Expand-Archive -Path actions-runner.zip -DestinationPath .
```

### 2. Configure the Runner

```powershell
# Configure the runner (replace with your repository URL and token)
.\config.cmd --url <https://github.com/your-org/your-repo> --token YOUR_RUNNER_TOKEN
```

### 3. Install as Service

```powershell
# Install the runner as a Windows service
.\svc-install.cmd
```

### 4. Start the Service

```powershell
# Start the runner service
.\svc-start.cmd
```

## Configuration Options

### Environment Variables

Set these environment variables for custom configuration:

```powershell
# Set environment variables
$env:RUNNER_NAME = "my-runner"
$env:RUNNER_WORKDIR = "C:\actions-runner\_work"
$env:RUNNER_LABELS = "self-hosted,windows,x64"
```

### Runner Labels

Configure labels for job targeting:

- `self-hosted`: Required for self-hosted runners
- `windows`: Operating system
- `x64`: Architecture
- Custom labels: `gpu`, `docker`, etc.

## Workflow Configuration

### Using Self-Hosted Runners

In your GitHub Actions workflow files:

```yaml
jobs:
  test:
    runs-on: self-hosted
    steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: |
        # Your test commands here
```

### Runner Groups

For organization-level runners, configure runner groups:

```yaml
jobs:
  test:
    runs-on: [self-hosted, windows]
    steps:
    - uses: actions/checkout@v4
```

## Maintenance

### Updating the Runner

```powershell
# Stop the service
.\svc-stop.cmd

# Update the runner
.\update.cmd

# Restart the service
.\svc-start.cmd
```

### Logs

Runner logs are located in:

- `C:\actions-runner\_diag\*.log`

### Troubleshooting

Common issues:

1. **Service won't start**: Check permissions and firewall settings
2. **Jobs not picking up runner**: Verify labels match workflow requirements
3. **Network issues**: Ensure GitHub connectivity (<https://github.com>)

## Security Considerations

- Run as non-administrative user when possible
- Limit runner access to necessary repositories only
- Regularly update runner software
- Monitor runner usage and logs
- Use runner groups for access control

## Uninstallation

To remove the runner:

```powershell
# Stop and remove the service
.\svc-uninstall.cmd

# Remove the directory
Remove-Item C:\actions-runner -Recurse -Force
```
