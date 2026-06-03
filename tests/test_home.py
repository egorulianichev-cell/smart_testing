def test_home_page_is_accessible(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"OK" in response.data
