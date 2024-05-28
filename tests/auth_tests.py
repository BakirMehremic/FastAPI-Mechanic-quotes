from tests import client
from app.services.users_auth import create_access_token
from app.db.models import Request, Quote, User, Mechanic
from app.db.database import SessionLocal


db = SessionLocal()


"""
    This file contains a few tests regarding user/mechanic
    required routes
"""


def create_test_users():
    exists = db.query(User).filter(User.user_id == 0).first()
    if not exists:
        user = User(user_id=0, username="testusernameuser",
                    hashed_password="test", name="test")
        db.add(user)
        db.commit()
    exists = db.query(Mechanic).filter(Mechanic.mechanic_id == 0).first()
    if not exists:
        mechanic = Mechanic(mechanic_id=0, username="exampleusernamemechanic",
                            hashed_password="test", contact_number=123)
        db.add(mechanic)
        db.commit()


# execute to add user and mechanic used for testing
create_test_users()


def create_user_token() -> str:
    return create_access_token(username="testusernameuser", user_id=0)


def create_mechanic_token():
    return create_access_token(username="exampleusernamemechanic", user_id=0)


"""
    some routes are limited to users or mechanics, but this is checked
    by the is_user function in each route so i only test it once for 
    mechanic and once for user
"""


def test_user_only():
    token = create_mechanic_token()
    response = client.delete("/auth/deleterequest/1",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_mechanic_only():
    token = create_user_token()
    response = client.delete("/auth/deletequote/1",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_invalid_request():
    token = create_user_token()
    # invalid because car is required
    response = client.post("/auth/newrequest",
                           headers={"Authorization": f"Bearer {token}"},
                           json={"mechanic_id": 0,
                                 "description": "test"})
    assert response.status_code == 422


def test_delete_request():
    token = create_user_token()
    to_delete = Request(user_id=0, mechanic_id=0, car="test")
    db.add(to_delete)
    db.commit()
    response = client.delete("/auth/deleterequest/0",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_delete_quote():
    token = create_mechanic_token()
    to_delete_request = Request(user_id=0, mechanic_id=0, car="test")
    db.add(to_delete_request)
    to_delete_quote = Quote(request_id=0, quote_id=0, amount=2222)
    db.add(to_delete_quote)
    db.commit()
    response = client.delete("/auth/deletequote/0",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
