def test_about_page_is_accessible(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"about" in response.data

def test_new_feature(client):
    response = client.get("/feature")
    assert response.status_code == 200
    assert b"New Feature" in response.data
