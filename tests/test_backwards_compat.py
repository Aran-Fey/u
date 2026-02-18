import u


def test_ton():
    # "ton" was renamed to "tonne"
    assert u.ton(3) == u.tonne(3)
    assert u.tons(3) == u.tonnes(3)
