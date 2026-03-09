import os

def test_describe_file(tmp_path):
    from importer import describe

    f = tmp_path / "hello.txt"
    f.write_text("abc")
    info = describe.describe_file(f)
    assert info["path"] == str(f)
    assert info["size"] == 3
