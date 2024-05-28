from tests import client
from app.services.admin_auth import create_access_token
from app.db.models import Request, Quote, User, Mechanic, Admin
from app.db.database import SessionLocal

db = SessionLocal()

"""
    This file contains tests regarding the admin endpoints
    - all tests pass with my db
"""


def create_test_admins():
    with_permissions = Admin(admin_id=0, username="testwithpermissions",
                             hashed_password="test", permissions="ALL")
    exists = db.query(Admin).filter(Admin.admin_id == 0).first()
    if not exists:
        db.add(with_permissions)
        db.commit()

    without_permissions = Admin(admin_id=9999, username="testwithoutpermissions",
                                hashed_password="test", permissions="PARTIAL")
    exists = db.query(Admin).filter(Admin.admin_id == 9999).first()
    if not exists:
        db.add(without_permissions)
        db.commit()


# execute to insert test adminds in db
create_test_admins()


def create_token_with_permissions() -> str:
    return create_access_token(username="testwithpermissions",
                               admin_id=0)


def create_token_without_permissions() -> str:
    return create_access_token(username="testwithoutpermissions",
                               admin_id=9999)


# this route requires admin permissions being set to all
def test_create_route():
    token = create_token_without_permissions()
    response = client.post("/admin/add",
                           headers={"Authorization": f"Bearer {token}"},
                           json={"username": "admin",
                                 "password": "PASSWORD",
                                 "permissions": "all"})
    assert response.status_code == 401


def test_delete_request():
    token = create_token_with_permissions()
    exists = db.query(Request).filter(Request.request_id == 0).first()
    if not exists:
        test_request = Request(request_id=0, mechanic_id=3, user_id=3, car="test")
        db.add(test_request)
        db.commit()
    response = client.delete("/admin/delete/request/0",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


# a bit more logic because sometimes tests fail and leave data in the db
def test_delete_quote():
    token = create_token_with_permissions()
    # a quote needs a valid request to exist, it is deleted along with the quote
    exists_quote = db.query(Quote).filter(Quote.request_id == 0).first()
    exists_request = db.query(Request).filter(Request.request_id == 0).first()
    test_request = Request(request_id=0, mechanic_id=2, user_id=1, car="test request")
    test_quote = Quote(quote_id=0, request_id=0, amount=0)
    if not exists_request:
        db.add(test_request)
        db.commit()
    if not exists_quote:
        db.add(test_quote)
        db.commit()
    response = client.delete("/admin/delete/quote/0",
                             headers={"Authorization": f"Bearer {token}"})
    if db.query(Quote).filter(Quote.quote_id == 0).first():
        db.delete(test_quote)
        db.commit()
    assert response.status_code == 200


def test_delete_mechanic():
    token = create_token_with_permissions()
    exists = db.query(Mechanic).filter(Mechanic.mechanic_id == 0).first()
    if not exists:
        to_delete = Mechanic(mechanic_id=0, hashed_password="test",
                             username="test username", contact_number=123)
        db.add(to_delete)
        db.commit()
    response = client.delete("/admindelete/mechanic/0",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_delete_user():
    token = create_token_with_permissions()
    exists = db.query(User).filter(User.user_id == 0).first()
    if not exists:
        to_delete = User(user_id=0, hashed_password="password",
                         username="test username", name="test name")
        db.add(to_delete)
        db.commit()
    response = client.delete("/admindelete/user/0",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_view_users():
    token = create_token_with_permissions()
    response = client.get("/admin/view/users",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_view_requests():
    token = create_token_with_permissions()
    response = client.get("/admin/view/requests",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_view_quotes():
    token = create_token_with_permissions()
    response = client.get("/admin/view/quotes",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200



