def test_generate_milestones(tmp_path):
    from roadmap import milestones

    out = tmp_path / "roadmap.md"
    milestones.create(out, ["Q1: start", "Q2: scale"])
    text = out.read_text()
    assert "Q1" in text and "Q2" in text
