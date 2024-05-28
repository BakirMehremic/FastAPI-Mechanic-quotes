from fastapi import status
from fastapi.exceptions import HTTPException
from db.models import Mechanic, User
from dependencies import db_dependency
from db.schemas import CreateMechanicRequest, CreateUserRequest
from core.config import settings


"""
    The route logic which donesnt require authorization - doesnt require user dependency
    are located in this file
"""


def singup_user_logic(db: db_dependency,
                      create_user_request: CreateUserRequest):
    exists_mech = db.query(Mechanic).filter(Mechanic.username == create_user_request.username).first()
    exists_user = db.query(User).filter(User.username == create_user_request.username).first()
    if exists_user or exists_mech:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Username is already taken")

    create_user = User(hashed_password=settings.bcrypt_context.hash(create_user_request.password),
                       username=create_user_request.username,
                       name=create_user_request.username)

    # contact number is optional
    if create_user_request.contact_number:
        create_user.contact_number = create_user_request.contact_number

    db.add(create_user)
    db.commit()

    return create_user


def signup_mechanic_logic(db: db_dependency,
                          create_mechanic_request: CreateMechanicRequest):
    exists_mech = db.query(Mechanic).filter(Mechanic.username == create_mechanic_request.username).first()
    exists_user = db.query(User).filter(User.username == create_mechanic_request.username).first()
    if exists_user or exists_mech:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Username is already taken")

    create_mechanic = Mechanic(username=create_mechanic_request.username,
                               hashed_password=settings.bcrypt_context.hash(create_mechanic_request.password),
                               contact_number=create_mechanic_request.contact_number)

    # address and workshop are optional
    if create_mechanic_request.address:
        create_mechanic.address = create_mechanic_request.address
    if create_mechanic_request.workshop:
        create_mechanic.workshop = create_mechanic_request.workshop

    db.add(create_mechanic)
    db.commit()

    return create_mechanic


# returns a list of all mechanics
def view_mechanics_logic(db):
    mechanics = db.query(Mechanic).all()
    if mechanics:
        return mechanics
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No mechanics found")


def view_mechanic_logic(mechanic_id, db):
    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()
    if mechanic:
        return mechanic
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No mechanic under this id")
