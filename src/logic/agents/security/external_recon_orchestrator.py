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

import asyncio
import os
import shutil
from typing import List, Optional
from dataclasses import dataclass

# Refactoring Note: Workflow ported from .external/0xSojalSec-AutoRecon/recon.sh
# This orchestration replaces the bash script with a Pythonic, async-capable flow.
# Actual binaries (nuclei, amass, etc.) must be installed in the system path.

@dataclass
class ReconConfig:
    domain: str
    results_path: str = "./results"
    use_amass: bool = True
    use_nuclei: bool = True
    threads: int = 5

class ExternalReconOrchestrator:
    """
    Orchestrates external security tools similar to AutoRecon.
    """
    def __init__(self, config: ReconConfig):
        self.config = config
        self.domain_dir = os.path.join(self.config.results_path, self.config.domain)
        os.makedirs(self.domain_dir, exist_ok=True)

    async def run_command(self, cmd: str, output_file: Optional[str] = None):
        """
        Run a shell command asynchronously and stream output.
        """
        print(f"[*] Running: {cmd}")
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if stdout and output_file:
            with open(output_file, 'wb') as f:
                f.write(stdout)
        
        if process.returncode != 0:
            print(f"[!] Command failed: {cmd}")
            print(f"[!] Error: {stderr.decode()}")
        else:
            print(f"[+] Command finished: {cmd}")

    async def run_amass(self):
        """
        Run Amass for subdomain enumeration.
        """
        if not shutil.which("amass"):
            print("[!] Amass not found in PATH")
            return

        cmd = f"amass enum -d {self.config.domain} -active -o {self.domain_dir}/amass.txt"
        await self.run_command(cmd)

    async def run_httprobe(self):
        """
        Run httprobe to find alive hosts.
        """
        if not shutil.which("httprobe"):
            print("[!] httprobe not found")
            return
        
        input_file = f"{self.domain_dir}/amass.txt"
        output_file = f"{self.domain_dir}/httprobe.txt"
        
        if not os.path.exists(input_file):
            print("[!] No input for httprobe")
            return

        # cat domains | httprobe
        cmd = f"type {input_file} | httprobe -p http:81 -p https:81" if os.name == 'nt' else f"cat {input_file} | httprobe"
        # Note: 'type' is windows equivalent of 'cat'
        
        await self.run_command(cmd, output_file)

    async def run_nuclei(self):
        """
        Run Nuclei scanner.
        """
        if not shutil.which("nuclei"):
            print("[!] Nuclei not found")
            return

        input_file = f"{self.domain_dir}/httprobe.txt"
        output_file = f"{self.domain_dir}/nuclei_report.txt"

        if not os.path.exists(input_file):
            print("[!] No input for nuclei")
            return

        cmd = f"nuclei -l {input_file} -o {output_file}"
        await self.run_command(cmd)

    async def execute_full_scan(self):
        """
        Execute the full recon pipeline.
        """
        if self.config.use_amass:
            await self.run_amass()
        
        await self.run_httprobe()
        
        if self.config.use_nuclei:
            await self.run_nuclei()

# Example usage
# if __name__ == "__main__":
#     config = ReconConfig(domain="example.com")
#     orchestrator = ExternalReconOrchestrator(config)
#     asyncio.run(orchestrator.execute_full_scan())
