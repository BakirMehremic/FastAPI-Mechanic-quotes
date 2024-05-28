from fastapi import status
from tests import client

"""
    this file contains a few simple tests
    which dont require authentification
    - all tests pass with my db
"""


def test_view_mechanic():
    response = client.get("/mechanic/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "username": "exampleusername d",
        "workshop": "some workshop name", "contact_number": 387123, "address": "Street 123"
    }


def test_view_all_mechanics():
    response = client.get("/mechanics")
    assert response.status_code == status.HTTP_200_OK


def test_view_nonex_mechanic():
    response = client.get("/mechanic/000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "No mechanic under this id"}


def test_nonex_login():
    response = client.post("/auth/token", data={"username": "test", "password": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Wrong username or password"
    }


# assuming the user exists
def test_login():
    response = client.post("/auth/token", data={"username": "exampleusernameuser",
                                                "password": "your password"})
    assert response.status_code == status.HTTP_200_OK

    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


