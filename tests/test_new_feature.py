def test_new_feature(client):
    response = client.get("/feature")
    assert response.status_code == 200
    assert b"New Feature" in response.data