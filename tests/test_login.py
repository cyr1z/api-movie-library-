import json

import pytest
from flask_login import current_user

from app.config import ADMIN_PASSWORD


@pytest.mark.parametrize(
    "test_arg, expected",
    [
        ("admin", ADMIN_PASSWORD),
    ],
)
def test_login(client, test_arg, expected):
    response = client.post(
        "/login",
        data=json.dumps(dict(username=test_arg, password=expected)),
        content_type="application/json",
    )

    data = json.loads(response.data)
    assert data["data"]["message"] == "login success"
    assert response.status_code == 200
    assert current_user.is_authenticated is True
    assert current_user.username == test_arg


def test_logout(client):
    response = client.post(
        "/logout",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert current_user.is_authenticated is False
