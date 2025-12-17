# Optional Tools for DebVisor\n\nDebVisor is built on Debian, but many other Linux

distributions

offer excellent tools that can enhance the administrator experience. Below is a
list of
recommended
optional tools to install.\n\n## System Monitoring & Diagnostics\n\n- **htop**:
Interactive process
viewer (better top).\n\n- **iotop**: Simple top-like I/O monitor.\n\n-
**iftop**: Display
bandwidth
usage on an interface by host.\n\n- **nmon**: Tuner and performance
monitor.\n\n-
**glances**:
Cross-platform system monitoring tool.\n\n- **btop**: Resource monitor that
shows usage
and stats
for processor, memory, disks, network and processes.\n\n## Storage
Management\n\n-
**ncdu**: NCurses
Disk Usage - great for finding what's eating disk space.\n\n- **parted**: Disk
partitioning and
partition resizing.\n\n- **smartmontools**: Control and monitor storage systems
using the
Self-Monitoring, Analysis and Reporting Technology System (SMART).\n\n## Network
Utilities\n\n-
**tcpdump**: Command-line packet analyzer.\n\n- **nmap**: Network exploration
tool and
security /
port scanner.\n\n- **mtr**: Network diagnostic tool that combines the
functionality of
traceroute
and ping.\n\n- **iperf3**: Tool for active measurements of the maximum
achievable
bandwidth on IP
networks.\n\n- **ethtool**: Query or control network driver and hardware
settings.\n\n##
Terminal
Multiplexers & Shell Enhancements\n\n- **tmux**: Terminal multiplexer.\n\n-
**screen**:
Full-screen
window manager that multiplexes a physical terminal.\n\n- **bash-completion**:
Programmable
completion for the bash shell.\n\n- **zsh**+**oh-my-zsh**: A powerful shell with
many
plugins.\n\n##
File Management & Editing\n\n- **mc (Midnight Commander)**: Visual file
manager.\n\n-
**vim**/**neovim**: Highly configurable text editor.\n\n- **nano**: Easy-to-use
text
editor (usually
installed by default).\n\n- **jq**: Command-line JSON processor.\n\n- **yq**:
Command-line
YAML
processor.\n\n## Virtualization & Containers\n\n- **virt-top**: 'top'-like
utility for
virtualization stats.\n\n- **guestfs-tools**: Tools to access and modify virtual
machine
disk
images.\n\n## Development & Maintenance Tools\n\n-
**scripts/fix_markdown_lint_comprehensive.py**: A
custom Python script included in this repository to automatically fix common
Markdown
linting errors
(MD022, MD031, MD032, etc.).\n\n- Usage: `python
scripts/fix_markdown_lint_comprehensive.py`\n\n-
**gh (GitHub CLI)**: Essential for managing workflows, issues, and pull requests
from the
command
line.\n\n- **act**: Run GitHub Actions locally (useful for testing workflows
before
pushing).\n\n##
Installation\n\nYou can install these tools using `apt`:\n\n```bash\napt
update\napt
install htop
iotop iftop ncdu tmux tcpdump nmap mtr-tiny iperf3 jq\n\n```python\n\napt
install htop
iotop iftop
ncdu tmux tcpdump nmap mtr-tiny iperf3 jq\n\n```python\napt update\napt install
htop iotop
iftop
ncdu tmux tcpdump nmap mtr-tiny iperf3 jq\n\n```python\n\napt install htop iotop
iftop
ncdu tmux
tcpdump nmap mtr-tiny iperf3 jq\n\n```python\napt update\napt install htop iotop
iftop
ncdu tmux
tcpdump nmap mtr-tiny iperf3 jq\n\n```python\n\napt install htop iotop iftop
ncdu tmux
tcpdump nmap
mtr-tiny iperf3 jq\n\n```python\napt install htop iotop iftop ncdu tmux tcpdump
nmap
mtr-tiny iperf3
jq\n\n```python\n\n```python\n\n
