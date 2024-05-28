from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from db.models import User, Mechanic, Request, Quote, Admin
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from db.schemas import CreateAdmin
from services.admin_auth import create_access_token, authenticate_user
from dependencies import db_dependency, admin_dependency
from core.config import settings
from utils import has_permissions


"""
    All the logic for admin endpoints is here
"""


# returns jwt tokens for admin users
def admin_login_for_access_token_logic(db: db_dependency,
                                       form_data: OAuth2PasswordRequestForm = Depends()):
    admin = authenticate_user(form_data.username, form_data.password, db)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong username or password")

    token = create_access_token(admin.username, admin.admin_id)

    return {"access_token": token, "token_type": "bearer"}


def delete_quote_logic(admin: admin_dependency, db: db_dependency,
                       quote_id: int):
    if not has_permissions(admin, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You only have partial permissions")

    quote = db.query(Quote).filter(Quote.quote_id == quote_id).first()

    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No quote with this id")

    db.delete(quote)
    db.commit()

    return {"deleted quote with id: ": quote_id}


def delete_request_logic(request_id: int, admin: admin_dependency,
                         db: db_dependency):
    if not has_permissions(admin, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You only have partial permissions")

    request = db.query(Request).filter(Request.request_id == request_id).first()

    if request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No quote with this id")

    # deleting related quotes because of foreign key constraints
    if request.quotes:
        for quote in request.quotes:
            db.delete(quote)
            db.commit()

    db.delete(request)
    db.commit()

    return {"deleted request with id": request_id}


def delete_user_logic(user_id: int,
                      admin: admin_dependency, db: db_dependency):
    if not has_permissions(admin, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You only have partial permissions")

    user_to_delete = db.query(User).filter(User.user_id == user_id).first()

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No user with this id")

    if user_to_delete.requests is None:
        db.delete(user_to_delete)
        db.commit()
        return {"deleted user with no requests, id": user_id}

    for request in user_to_delete.requests:
        for quote in request.quotes:
            db.delete(quote)
            db.commit()
        db.delete(request)
        db.commit()

    db.delete(user_to_delete)
    db.commit()

    return {"deleted user with id": user_id}


def delete_mechanic_logic(mechanic_id: int,
                          admin: admin_dependency, db: db_dependency):
    if not has_permissions(admin, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You only have partial permissions")

    mech_to_delete = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()

    if mech_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No mechanic with this id")

    if mech_to_delete.requests is None:
        db.delete(mech_to_delete)
        db.commit()
        return {"deleted mechanic with id": mechanic_id}

    for request in mech_to_delete.requests:
        for quote in request.quotes:
            db.delete(quote)
            db.commit()
        db.delete(request)
        db.commit()

    db.delete(mech_to_delete)
    db.commit()

    return {"deleted mechanic with id": mechanic_id}


def add_admin_logic(db: db_dependency, admin: admin_dependency,
                    create_admin_data: CreateAdmin):
    if not has_permissions(admin, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only admins with all permissions can create new")
    exists = db.query(Admin).filter(Admin.username == create_admin_data.username).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="This username is taken")

    admin = Admin(username=create_admin_data.username,
                  hashed_password=settings.bcrypt_context.hash(create_admin_data.password),
                  permissions=create_admin_data.permissions)

    db.add(admin)
    db.commit()

    return admin


# admin dependency is already handled in routes
def view_users_logic(db: db_dependency, user_id: Optional[int] = None):
    if user_id:
        user_to_view = db.query(User).filter(User.user_id == user_id).first()
        if user_to_view:
            return user_to_view
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No user with this id")

    users = db.query(User).all()
    return users


# admin dependency is already handled in routes
def view_requests_logic(db: db_dependency, request_id: Optional[int] = None):
    if request_id:
        request = db.query(Request).filter(Request.request_id == request_id).first()
        if request:
            return request
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No request with this id")

    requests = db.query(Request).all()
    return requests


# admin dependency is already handled in routes
def view_quotes_logic(db: db_dependency, quote_id: Optional[int] = None):
    if quote_id:
        quote = db.query(Quote).filter(Quote.quote_id == quote_id).first()
        if quote:
            return quote
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No quote with this id")

    quotes = db.query(Quote).all()
    return quotes
