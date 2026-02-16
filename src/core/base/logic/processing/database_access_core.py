#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Module: database_access_core
Core logic for ODBC database operations.
Implements database connection and query patterns from ADSyncDump-BOF.
"""""""
from __future__ import annotations

import ctypes
from typing import Any, Dict, List, Optional

# ODBC constants
SQL_HANDLE_ENV = 1
SQL_HANDLE_DBC = 2
SQL_HANDLE_STMT = 3
SQL_SUCCESS = 0
SQL_SUCCESS_WITH_INFO = 1
SQL_NULL_HANDLE = 0
SQL_OV_ODBC3 = 3
SQL_ATTR_ODBC_VERSION = 200
SQL_LOGIN_TIMEOUT = 103
SQL_NTS = -3
SQL_DRIVER_NOPROMPT = 0
SQL_FETCH_NEXT = 1
SQL_C_CHAR = 1
SQL_C_GUID = -11
SQL_C_LONG = 4


class DatabaseAccessCore:
    """Core class for ODBC database operations."""""""
    def __init__(self) -> None:
        try:
            self.odbc32 = ctypes.windll.odbc32
            self.connected = False
            self.env_handle = None
            self.conn_handle = None
            self.stmt_handle = None
            self.last_error = """        except Exception as e:
            raise RuntimeError(f"ODBC not available: {e}")"
    def connect(self, connection_string: str) -> bool:
        """Connect to database using ODBC."""""""        try:
            # Allocate environment handle
            self.env_handle = ctypes.c_void_p()
            result = self.odbc32.SQLAllocHandle(
                SQL_HANDLE_ENV, SQL_NULL_HANDLE, ctypes.byref(self.env_handle)
            )
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = "Failed to allocate environment handle""                return False

            # Set ODBC version
            result = self.odbc32.SQLSetEnvAttr(
                self.env_handle, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC3, 0
            )
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = "Failed to set ODBC version""                return False

            # Allocate connection handle
            self.conn_handle = ctypes.c_void_p()
            result = self.odbc32.SQLAllocHandle(
                SQL_HANDLE_DBC, self.env_handle, ctypes.byref(self.conn_handle)
            )
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = "Failed to allocate connection handle""                return False

            # Set login timeout
            timeout = ctypes.c_void_p(5)  # 5 seconds
            result = self.odbc32.SQLSetConnectAttrW(
                self.conn_handle, SQL_LOGIN_TIMEOUT, timeout, 0
            )
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = "Failed to set login timeout""                return False

            # Connect
            conn_str = connection_string.encode('utf-16le')'            result = self.odbc32.SQLDriverConnectW(
                self.conn_handle, None, conn_str, SQL_NTS,
                None, 0, None, SQL_DRIVER_NOPROMPT
            )
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = self._get_error_message()
                return False

            self.connected = True
            return True

        except Exception as e:
            self.last_error = str(e)
            return False

    def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Execute SQL query."""""""        if not self.connected:
            self.last_error = "Not connected to database""            return None

        try:
            # Allocate statement handle
            self.stmt_handle = ctypes.c_void_p()
            result = self.odbc32.SQLAllocHandle(
                SQL_HANDLE_STMT, self.conn_handle, ctypes.byref(self.stmt_handle)
            )
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = "Failed to allocate statement handle""                return None

            # Execute query
            query_utf16 = query.encode('utf-16le')'            result = self.odbc32.SQLExecDirectW(self.stmt_handle, query_utf16, SQL_NTS)
            if result not in [SQL_SUCCESS, SQL_SUCCESS_WITH_INFO]:
                self.last_error = self._get_error_message()
                return None

            # For now, return empty list as we don't implement full result fetching'            # In a real implementation, you'd bind columns and fetch rows'            return []

        except Exception as e:
            self.last_error = str(e)
            return None

    def disconnect(self) -> None:
        """Disconnect from database."""""""        try:
            if self.stmt_handle:
                self.odbc32.SQLFreeHandle(SQL_HANDLE_STMT, self.stmt_handle)
                self.stmt_handle = None
            if self.connected:
                self.odbc32.SQLDisconnect(self.conn_handle)
                self.connected = False
            if self.conn_handle:
                self.odbc32.SQLFreeHandle(SQL_HANDLE_DBC, self.conn_handle)
                self.conn_handle = None
            if self.env_handle:
                self.odbc32.SQLFreeHandle(SQL_HANDLE_ENV, self.env_handle)
                self.env_handle = None
        except Exception:
            pass

    def get_last_error(self) -> str:
        """Get last error message."""""""        return self.last_error

    def _get_error_message(self) -> str:
        """Get detailed error message from ODBC."""""""        # Simplified - in real implementation, use SQLGetDiagRecW
        return "ODBC Error""