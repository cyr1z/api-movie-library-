import json

from flask_login import current_user

from app.config import ADMIN_PASSWORD

film = {
    "rate": 5,
    "description": "movie1",
    "name": "movie1",
    "poster_link": "http://google.com/movie1.jpg",
    "released": "2014-10-22",
    "production": "prod",
    "genres": [
        "Comedy"
    ],
    "directors": [
        "Tarantino"
    ],
    "country_name": "USA",
    "country_short": "US"
}


def test_movie_post_and_delete(client):
    client.post(
        "/login",
        data=json.dumps(dict(username='admin', password=ADMIN_PASSWORD)),
        content_type="application/json",
    )
    assert current_user.is_authenticated is True

    response = client.post(
        "/movies",
        data=json.dumps(dict(film)),
        content_type="application/json",
    )
    data = json.loads(response.data)
    assert response.status_code == 201
    new_id = data["id"]
    assert data["name"] == film["name"]

    delete_response = client.delete(f"/movies/{new_id}")
    assert delete_response.status_code == 200

    client.post(
        "/logout",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert current_user.is_authenticated is False
