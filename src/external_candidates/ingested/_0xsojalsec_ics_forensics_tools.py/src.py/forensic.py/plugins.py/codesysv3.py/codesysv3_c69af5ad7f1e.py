# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\plugins\CodeSysV3\CodeSysV3.py
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from forensic.analyzers.CodeSysV3 import app_parser
from forensic.common.constants.constants import Transport
from forensic.interfaces.plugin import PluginCLI, PluginConfig, PluginInterface
from forensic.plugins.CodeSysV3.codesysv3_protocol import *
from tenacity import retry, retry_if_exception_type, stop_after_attempt


class CodeSysV3CLI(PluginCLI):
    def __init__(self, folder_name):
        super().__init__(folder_name)
        self.name = "CodeSysV3"
        self.description = "CodeSysV3 Plugin"
        self.port = 11740
        self.transport = Transport.TCP

    def flags(self, parser):
        self.base_flags(parser, self.port, self.transport)
        parser.add_argument(
            "--src_ip",
            help="SrcIP",
            metavar="",
            const=socket.gethostbyname(socket.gethostname()),
            nargs="?",
        )


class CodeSysV3(PluginInterface):
    def __init__(self, config: PluginConfig, output_dir: Path, verbose: bool):
        super().__init__(config, output_dir, verbose)
        self.port = config.parameters.get("port")
        self.transport = config.parameters.get("transport")

    @retry(
        retry=(
            retry_if_exception_type(TimeoutError) | retry_if_exception_type(Exception)
        ),
        stop=stop_after_attempt(3),
    )
    def _conn(self, files, address):
        data_files_dir = self.output_dir.joinpath("CS3RawFileParser")

        try:
            with CodeSysV3Device(address["ip"], address["src_ip"]) as device:
                with device.open_channel() as channel:
                    channel.login(address["username"], address["password"])
                    fileapi = FilesTransfer(channel)
                    plc_files = fileapi.dir("$PlcLogic$")
                    for fname in plc_files:
                        app_name = os.path.basename(fname).rpartition(".")[0]
                        app_files_dir = Path(
                            os.path.join(
                                data_files_dir,
                                address["ip"].replace(".", "_"),
                                app_name,
                            )
                        )
                        app_files_dir.mkdir(parents=True, exist_ok=True)
                        fileapi.download(
                            "$PlcLogic$/" + fname,
                            Path(os.path.join(app_files_dir, fname)),
                        )
                        if fname.endswith(".app"):
                            files[address["ip"]].append(
                                os.path.join(app_files_dir, fname)
                            )
        except socket.timeout:
            self.logger.info(
                f"Timeout error for IP: {address}, "
                f"Port: {self.config.port}, Protocol_type: {self.config.transport}"
            )
            raise TimeoutError
        except Exception as e:
            self.logger.exception(
                f"{e} for IP: {address}, "
                f"Port: {self.config.port}, Protocol_type: {self.config.transport}"
            )
            raise

    def connect(self, address: dict):
        files = defaultdict(list)
        with ThreadPoolExecutor(max_workers=30) as executor:
            executor.submit(self._conn, files, address)
        return files

    def export(self, extracted):
        super().export(extracted)
