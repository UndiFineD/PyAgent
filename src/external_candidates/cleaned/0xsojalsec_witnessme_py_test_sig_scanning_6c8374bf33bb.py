# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_witnessme.py\tests.py\test_sig_scanning_6c8374bf33bb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-WitnessMe\tests\test_sig_scanning.py

import pytest

from witnessme.signatures import Signatures


@pytest.fixture
def sig_eng():

    return Signatures()


@pytest.fixture
def sig_eng_l():

    s = Signatures()

    s.load()

    return s


def test_sig_load(sig_eng):

    sig_eng.load()

    assert len(sig_eng.signatures) > 0


def test_get_sig_name(sig_eng_l):

    s = sig_eng_l.get_sig("ADManager")

    print(s)

    assert s != None


@pytest.mark.asyncio
async def test_signature_scanning(sig_eng_l):

    # Simulates an html page

    service_html = """<html>

<body>

<div>

ADManager Plus Authentication

\n\rManageEngine\n\r

</div>

<script src="js/framework/Hashtable.js">

sel.options[i].text == 'ADManager Plus Authentication'

</script>

\r\r\r

</body>

</html>"""

    fake_service = (0, "http://fakeurl:port/", service_html)

    matches, _ = await sig_eng_l.find_match(fake_service)

    print(matches)

    assert len(matches) == 1

    assert matches[0]["name"] == "ADManager"
