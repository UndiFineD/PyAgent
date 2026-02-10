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

import os
import subprocess
import shutil
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, wait

logger = logging.getLogger(__name__)


class NucleiTemplateCollector:
    """
    Collects Nuclei templates from various public repositories.
    Adapted from AllForOne tool.
    """

    DEFAULT_SOURCE_LIST = 'https://raw.githubusercontent.com/AggressiveUser/AllForOne/main/PleaseUpdateMe.txt'

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "_temp_clones")

    def _git_clone(self, url, destination):
        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'
        try:
            result = subprocess.run(
                ['git', 'clone', url, destination],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                env=env,
                check=False
            )
            return result.returncode, result.stderr.decode().strip()
        except Exception as e:
            return 1, str(e)

    def _generate_destination_folder(self, url):
        folder_name = os.path.basename(url.rstrip('.git'))
        counter = 1
        base_path = os.path.join(self.temp_dir, folder_name)
        while os.path.exists(base_path):
            folder_name = f"{os.path.basename(url.rstrip('.git'))}_{counter}"
            base_path = os.path.join(self.temp_dir, folder_name)
            counter += 1
        return folder_name

    def _clone_repository(self, repo):
        folder_name = self._generate_destination_folder(repo)
        destination = os.path.join(self.temp_dir, folder_name)
        return_code, error_msg = self._git_clone(repo, destination)
        if return_code != 0:
            logger.warning(f"Failed to clone {repo}: {error_msg}")
            return repo
        return None

    def collect_templates(self, source_url: str = None):
        """
        Main execution method to collect templates.
        """
        source_url = source_url or self.DEFAULT_SOURCE_LIST

        try:
            response = requests.get(source_url, timeout=30)
            if response.status_code == 200:
                repositories = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
            else:
                logger.error(f'Failed to retrieve Repo List from {source_url}')
                return
        except Exception as e:
            logger.error(f"Error fetching source list: {e}")
            return

        total_repos = len(repositories)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        logger.info(f"Starting clone of {total_repos} repositories...")
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(self._clone_repository, repo) for repo in repositories]
            wait(futures)

        logger.info("Cloning complete. Extracting templates...")

        yaml_count = 0
        for root, dirs, files in os.walk(self.temp_dir):
            for file in files:
                if file.endswith('.yaml'):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(self.output_dir, file)
                    # Handle filename collisions? Currently overwrites or just dumps all in root
                    # The original script dumped all in one folder.
                    
                    # Let's try to preserve some structure or just rename if exists
                    if os.path.exists(destination_path):
                        base, ext = os.path.splitext(file)
                        destination_path = os.path.join(self.output_dir, f"{base}_{yaml_count}{ext}")

                    try:
                        shutil.copy2(source_path, destination_path)
                        yaml_count += 1
                    except Exception as e:
                        logger.error(f"Error copying {file}: {e}")

        logger.info(f"Collected {yaml_count} Nuclei templates to {self.output_dir}")

        # Cleanup
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                logger.warning(f"Failed to cleanup temp dir {self.temp_dir}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    collector = NucleiTemplateCollector(output_dir="collected_templates")
    collector.collect_templates()
