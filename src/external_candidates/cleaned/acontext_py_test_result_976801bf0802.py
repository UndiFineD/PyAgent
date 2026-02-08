# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\acontext.py\src.py\server.py\core.py\tests.py\schema.py\test_result_976801bf0802.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\Acontext\src\server\core\tests\schema\test_result.py

from acontext_core.schema.result import Code, Result

from fastapi.responses import JSONResponse


def test_result_class():

    test_data = {"message": "pong"}

    suc = Result.resolve(test_data)

    d, eil = suc.unpack()

    assert d == test_data

    assert eil is None

    err = Result.reject("test", Code.BAD_REQUEST)

    d, eil = err.unpack()

    assert d is None

    assert eil.status == Code.BAD_REQUEST
