def test_about_page_is_accessible(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"about" in response.data
