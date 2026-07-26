from game.challenges import get_challenges


def test_unique_ids():
    ids = [c.id for c in get_challenges()]
    assert len(ids) == len(set(ids))


def test_code_challenges_have_tests():
    for ch in get_challenges():
        if ch.kind == "code":
            assert ch.func_name
            assert ch.test_cases


def test_points_positive():
    for ch in get_challenges():
        assert ch.points > 0
