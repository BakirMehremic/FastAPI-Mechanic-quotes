from fastapi import APIRouter, Depends
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from db.schemas import CreateAdmin, Token
from dependencies import db_dependency, admin_dependency
from crud.admin import (add_admin_logic, admin_login_for_access_token_logic,
                        view_users_logic, view_quotes_logic, view_requests_logic,
                        delete_quote_logic, delete_user_logic, delete_request_logic,
                        delete_mechanic_logic)


admin_router = APIRouter(
    prefix="/admin",
    tags=["admin routes"]
)


# returns jwt tokens for admin users
@admin_router.post("/token", response_model=Token)
async def login_for_access_token(db:db_dependency,
                                 form_data: OAuth2PasswordRequestForm = Depends()):

    return admin_login_for_access_token_logic(db=db, form_data=form_data)


"""
    the following 4 routes require the admin permissions
    to be all - deleting users requests and quotes and creating new admins
"""


@admin_router.delete("/delete/quote/{quote_id}", summary="""
                     Irreversibly deleting quotes from db""")
async def delete_quote(admin: admin_dependency, db: db_dependency,
                       quote_id: int):
    
    delete_quote_logic(admin=admin, db=db, quote_id=quote_id)


@admin_router.delete("/delete/request/{request_id}", summary="""
              Deleting a request with all related quotes""")
async def delete_request(request_id: int, admin: admin_dependency,
                         db: db_dependency):
    return delete_request_logic(request_id=request_id, admin=admin, db=db)


@admin_router.delete("delete/user/{user_id}", summary="""
                     Deleting a user with all related quotes and requests""")
async def delete_user(user_id: int,
                       admin: admin_dependency, db: db_dependency):
    
    return delete_user_logic(user_id=user_id, admin=admin, db=db)



@admin_router.delete("delete/mechanic/{mechanic_id}", summary="""
                     Deleting a user with all related quotes and requests""")
async def delete_mechanic(mechanic_id: int,
                       admin: admin_dependency, db: db_dependency):
    
    return delete_mechanic_logic(mechanic_id=mechanic_id, admin=admin, db=db)



@admin_router.post("/add")
async def add_admin(db:db_dependency, admin: admin_dependency,
                    create_admin_data: CreateAdmin):
    
    add_admin_logic(db=db, admin=admin, create_admin_data=create_admin_data)



"""
    The routes for viewing users, requests and quotes
    can be accesed by all admin users regardless of permissions 
    - no route for viewing mechanics because it exists in no auth routes
"""


@admin_router.get("/view/users")
async def view_users(db: db_dependency,
                     user_id: Optional[int] = None):
    
    view_users_logic(db=db, user_id=user_id)


@admin_router.get("/view/requests")
async def view_requests(db: db_dependency,
                        request_id: Optional[int] = None):
    
    view_requests_logic(db=db, request_id=request_id)


@admin_router.get("/view/quotes")
async def view_quotes(db: db_dependency, quote_id: Optional[int] = None):
    
    view_quotes_logic(db=db, quote_id=quote_id)

