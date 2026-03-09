def test_record_experiment(tmp_path):
    from roadmap import innovation

    db = tmp_path / "experiments.json"
    path = innovation.record_experiment("test-exp", db_path=str(db))
    assert path.exists()
    data = path.read_text()
    assert "test-exp" in data
