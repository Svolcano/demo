from tools.utils import to_dict


def test_to_dict(user1):
    result = to_dict(user1)
    assert result["score"] == user1.score
