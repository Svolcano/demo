def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert "pong" in response.json()


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJib3NzIiwiZXhwIjoxNzE4OTYxMzAzfQ.NO5jvWnsQmcA2WM7TK4dogU1Aa5KHtFIDoy8srcQ5hs"
}


def test_userscore(client):

    response = client.post(
        "/user/score",
        json={"user_id": "1", "score_modifier": 2, "score": 123},
        headers=headers,
    )
    assert response.status_code == 200
    out = response.json()
    assert out["user_id"] == "1" and out["role"] == "staff"

    response = client.post(
        "/user/score",
        json={"user_id": "0", "score_modifier": 2, "score": 123},
        headers=headers,
    )
    assert response.status_code == 200
    out = response.json()
    assert out["user_id"] == "0" and out["role"] == "admin"


def test_invaliduser(client):
    response = client.post(
        "/user/score",
        json={"user_id": "110", "score_modifier": 2, "score": 123},
        headers=headers,
    )
    assert response.status_code == 400
