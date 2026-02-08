# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-mythic_mcp\lib\mythic_api.py
from mythic import mythic, mythic_classes


class MythicAPI:
    def __init__(self, username, password, server_ip, server_port):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.server_port = server_port

    async def connect(self):
        self.mythic_instance = await mythic.login(
            username=self.username,
            password=self.password,
            server_ip=self.server_ip,
            server_port=self.server_port,
        )

    async def execute_shell_command(self, agent_id, command) -> str:
        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                self.mythic_instance,
                command_name="shell",
                parameters=command,
                callback_display_id=agent_id,
            )
            return str(output)
        except Exception as e:
            return "Error: Could not execute command: {}".format(command)

    async def read_file(self, agent_id, file_path) -> str:
        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                self.mythic_instance,
                command_name="cat",
                callback_display_id=agent_id,
                parameters={"path": file_path},
            )

            return output.decode()

        except Exception as e:
            return "Error: Could not read file: {}".format(e)

    async def make_token(self, agent_id, username, password) -> bool:
        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                self.mythic_instance,
                command_name="make_token",
                callback_display_id=agent_id,
                parameters={"username": username, "password": password},
            )

            return True

        except Exception as e:
            return False

    async def execute_mimikatz(self, agent_id, mimikatz_command) -> str | None:
        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                self.mythic_instance,
                command_name="mimikatz",
                callback_display_id=agent_id,
                parameters={"commands": mimikatz_command},
            )

            return output.decode()

        except Exception as e:
            return None

    async def get_all_agents(self):
        try:
            agents = await mythic.get_all_active_callbacks(self.mythic_instance)
            return agents

        except Exception as e:
            return []

    async def download_file(self, agent_id, file_path):
        try:
            status = await mythic.issue_task(
                mythic=self.mythic_instance,
                command_name="download",
                parameters={"path": file_path},
                wait_for_complete=True,
                callback_display_id=agent_id,
            )
        except Exception as e:
            return None

    async def upload_file(self, agent_id, filename, file_path, contents) -> bool:
        try:
            file_id = await mythic.register_file(mythic=self.mythic_instance, filename=filename, contents=contents)

            status = await mythic.issue_task(
                mythic=self.mythic_instance,
                command_name="upload",
                parameters={"remote_path": file_path, "file": file_id},
                callback_display_id=agent_id,
                wait_for_complete=True,
            )

            if status["status"] == "success":
                return True
            else:
                return False

        except Exception as e:
            return False
