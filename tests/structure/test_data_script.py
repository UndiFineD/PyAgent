import os
from scripts.generate_test_data import generate_sample_fixture

def test_data_script(tmp_path):
    file = tmp_path / "fixture.json"
    generate_sample_fixture(str(file))
    assert file.read_text() == "{}"
