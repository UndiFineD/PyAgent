def test_vision_template_exists(tmp_path):
    from roadmap import vision

    # template function should return a non-empty string
    text = vision.get_template()
    assert isinstance(text, str) and "Vision" in text
