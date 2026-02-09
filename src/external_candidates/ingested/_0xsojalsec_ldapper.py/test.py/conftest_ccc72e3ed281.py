# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ldapper\test\conftest.py

import pytest

from .utils import Connection


@pytest.fixture(scope="module")
def connection():
    logindn = "cn=admin,dc=acme,dc=org"
    password = "JonSn0w"
    conn = Connection.connect(logindn=logindn, password=password)
    Connection.set_connection(conn)
    return conn
