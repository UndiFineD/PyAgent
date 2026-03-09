def test_score_feature():
    from roadmap import prioritization

    attrs = {"impact": 10, "effort": 2}
    score = prioritization.score_feature(attrs)
    assert isinstance(score, (int, float))
