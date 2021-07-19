import json

import pytest

from app.app import app
from app.resources.movies import ORDER_CHOICES


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "test_arg, expected",
    [
        (42, 200),
        (1, 200),
        ("100", 200),
    ],
)
def test_movie_get_by_id(client, test_arg, expected):
    response = client.get(f"/movies/{test_arg}")
    data = json.loads(response.data)
    assert response.status_code == expected
    assert data.get("id") == int(test_arg)


@pytest.mark.parametrize("test_arg", [-42, "one", 0, 0.42])
def test_movie_get_by_wrong_id(client, test_arg):
    response = client.get(f"/movies/{test_arg}")
    assert response.status_code == 404


def test_movie_get_default(client):
    response = client.get("/movies")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 10


@pytest.mark.parametrize("test_arg", [5, 10, 20])
def test_movie_get_page_size(client, test_arg):
    response = client.get(f"/movies?pageNumber=1&pageSize={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == test_arg


@pytest.mark.parametrize("test_arg", [5.6, 'dgdg6'])
def test_movie_get_page_size_wrong(client, test_arg):
    response = client.get(f"/movies?pageNumber=1&pageSize={test_arg}")
    data = json.loads(response.data)

    error = {
        "errors": {
            "pageSize": f"Page size invalid literal for int() with base 10: '{test_arg}'"
        }, "message": "Input payload validation failed"
    }
    assert response.status_code == 400
    assert data == error


@pytest.mark.parametrize("test_arg", [5, 10, 20])
def test_movie_get_page_number(client, test_arg):
    response = client.get(f"/movies?pageNumber={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 10


@pytest.mark.parametrize("test_arg", [5.6, 'dgdg6'])
def test_movie_get_page_number_wrong(client, test_arg):
    response = client.get(f"/movies?pageNumber={test_arg}")
    data = json.loads(response.data)

    error = {
        "errors": {
            "pageNumber": f"Page number invalid literal for int() "
                          f"with base 10: '{test_arg}'"
        }, "message": "Input payload validation failed"
    }
    assert response.status_code == 400
    assert data == error


@pytest.mark.parametrize(
    "test_arg, expected",
    [
        ("Pulp Fiction", "Quentin Tarantino"),
        ("Apocalypse Now", "Francis Ford Coppola"),
    ],
)
def test_movie_search(client, test_arg, expected):
    response = client.get(f"/movies?searchQuery={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data[0]['directors'][0]['name'] == expected


@pytest.mark.parametrize(
    "test_arg, expected",
    [
        (12, 1),
        (13, 7),
    ],
)
def test_movie_get_by_diretor_id(client, test_arg, expected):
    response = client.get(f"/movies?directorId={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data[0]['directors'][0]['id'] == test_arg
    assert len(data) == expected


@pytest.mark.parametrize(
    "test_arg, expected",
    [
        ("Simon McQuoid", 1),
        ("Adam Wingard", 7),
    ],
)
def test_movie_get_by_diretor_name(client, test_arg, expected):
    response = client.get(f"/movies?directorName={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data[0]['directors'][0]['name'] == test_arg
    assert len(data) == expected


@pytest.mark.parametrize("test_arg", ["Simonuoid", "Adamngard"])
def test_movie_get_by_diretor_wrong_name(client, test_arg):
    response = client.get(f"/movies?directorName={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data == {"Error": "Wrong Director name"}


@pytest.mark.parametrize("test_arg", ["Comedy", "Action"])
def test_movie_get_by_genre_name(client, test_arg):
    response = client.get(f"/movies?genreName={test_arg}")
    assert response.status_code == 200


@pytest.mark.parametrize("test_arg", [1, "qwerty"])
def test_movie_get_by_genre_wrong_name(client, test_arg):
    response = client.get(f"/movies?genreName={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data == {"Error": "Wrong Genre name"}


@pytest.mark.parametrize("test_arg", [1, 9])
def test_movie_get_by_genre_id(client, test_arg):
    response = client.get(f"/movies?genreId={test_arg}")
    assert response.status_code == 200


@pytest.mark.parametrize("test_arg", [-1, 12000000])
def test_movie_get_by_genre_wrong_1d(client, test_arg):
    response = client.get(f"/movies?genreId={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data == {"Error": "Wrong Genre ID"}


@pytest.mark.parametrize("test_arg", [1.9, 'qwerty'])
def test_movie_get_by_genre_non_numeric_1d(client, test_arg):
    response = client.get(f"/movies?genreId={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data == {
        "errors": {
            "genreId": f"Genre ID invalid literal for int() with "
                       f"base 10: '{test_arg}'"
        }, "message": "Input payload validation failed"
    }


@pytest.mark.parametrize("test_arg", [1987, 2000])
def test_movie_get_from_year(client, test_arg):
    response = client.get(f"/movies?yearFrom={test_arg}")
    assert response.status_code == 200


@pytest.mark.parametrize("test_arg", [12, 2121])
def test_movie_get_by_wrong_year_from(client, test_arg):
    response = client.get(f"/movies?yearFrom={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert "Wrong Year from." in data['Error']


@pytest.mark.parametrize("test_arg", [1.2, 'qwa'])
def test_movie_get_by_not_int_year_from(client, test_arg):
    response = client.get(f"/movies?yearFrom={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data == {
        "errors": {
            "yearFrom": "from year invalid literal for int() with "
                        f"base 10: '{test_arg}'"
        }, "message": "Input payload validation failed"
    }


@pytest.mark.parametrize("test_arg", [1987, 2000])
def test_movie_get_to_year(client, test_arg):
    response = client.get(f"/movies?yearTo={test_arg}")
    assert response.status_code == 200


@pytest.mark.parametrize("test_arg", [12, 2121])
def test_movie_get_by_wrong_year_to(client, test_arg):
    response = client.get(f"/movies?yearTo={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 404
    assert "Wrong Year to." in data['Error']


@pytest.mark.parametrize("test_arg", [1.2, 'qwa'])
def test_movie_get_by_not_int_year_to(client, test_arg):
    response = client.get(f"/movies?yearTo={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data == {
        "errors": {
            "yearTo": "to year invalid literal for int() with "
                      f"base 10: '{test_arg}'"
        }, "message": "Input payload validation failed"
    }


@pytest.mark.parametrize("test_arg", ORDER_CHOICES)
def test_movie_order(client, test_arg):
    response = client.get(f"/movies?orderBy={test_arg}")
    assert response.status_code == 200


@pytest.mark.parametrize("test_arg", [1.2, 12, 'year', 'krya'])
def test_movie_wrong_order(client, test_arg):
    response = client.get(f"/movies?orderBy={test_arg}")
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data == {
        "errors": {
            "orderBy": f"Bad order by choice The value '{test_arg}' is not "
                       "a valid choice for 'orderBy'."
        }, "message": "Input payload validation failed"
    }
