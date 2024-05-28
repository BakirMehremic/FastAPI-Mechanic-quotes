from fastapi import APIRouter, status
from dependencies import db_dependency
from db.schemas import CreateMechanicRequest,CreateUserRequest, ViewMechanic, ViewUser
from crud.no_auth import (singup_user_logic, signup_mechanic_logic,
                          view_mechanic_logic, view_mechanics_logic)


no_auth_router=(
    APIRouter(tags=["non-auth routes"]))


"""
The routes which dont require authorization - dont require user dependency
are located in this file
"""


@no_auth_router.post("/user/signup", status_code=status.HTTP_201_CREATED,
                     response_model=ViewUser)
async def singup_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    return singup_user_logic(db,create_user_request)


@no_auth_router.post("/mechanic/signup", status_code=status.HTTP_201_CREATED,
                     response_model=ViewMechanic)
async def signup_mechanic(db: db_dependency, 
                          create_mechanic_request: CreateMechanicRequest):
    return signup_mechanic_logic(db,create_mechanic_request)


# returns a list of all mechanics
@no_auth_router.get("/mechanics", response_model=list[ViewMechanic])
async def view_mechanics(db: db_dependency):
    return view_mechanics_logic(db)


@no_auth_router.get("/mechanic/{mechanic_id}", response_model=ViewMechanic)
async def view_mechanic(mechanic_id: int, db: db_dependency):
    return view_mechanic_logic(db=db, mechanic_id=mechanic_id)
