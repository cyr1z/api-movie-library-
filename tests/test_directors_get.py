import json

import pytest


@pytest.mark.parametrize(
    "test_arg, expected",
    [
        (42, 200),
        (1, 200),
        ("100", 200),
    ],
)
def test_director_get_by_id(client, test_arg, expected):
    response = client.get(f"/directors/{test_arg}")
    data = json.loads(response.data)
    assert response.status_code == expected
    assert data.get("id") == int(test_arg)


@pytest.mark.parametrize("test_arg", [-42, "one", 0, 0.42])
def test_director_get_by_wrong_id(client, test_arg):
    response = client.get(f"/directors/{test_arg}")
    assert response.status_code == 404


def test_directors_get_default(client):
    response = client.get("/directors")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 10
