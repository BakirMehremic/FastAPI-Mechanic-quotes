from fastapi import APIRouter, Depends, status
from dependencies import db_dependency, user_dependency
from fastapi.security import OAuth2PasswordRequestForm
from db.schemas import (NewRequest, NewQuote, AcceptOrDecline,
                        ViewQuote, ViewRequest, EditMechanic, EditUser,
                        ViewMechanic, ViewUser, Token)
from crud.auth import (login_for_access_token_logic, delete_quote_logic,
                       delete_request_logic, my_requests_logic,
                       new_quote_logic, new_request_logic, accept_or_decline_quote_logic,
                       edit_user_profile_logic, edit_mechanic_profile_logic)


"""
    all the routes which require user authentification
    are in this file, the logic is in services.user_auth

    the authorization is done in the way fastapi recommends
"""

auth_router=APIRouter(
    prefix="/auth",
    tags=["users - auth"]
)


# returns jwt tokens for both users and mechanics
@auth_router.post("/token", response_model=Token)
async def login_for_access_token(db: db_dependency,
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    return login_for_access_token_logic(db, form_data)


@auth_router.post("/newrequest", response_model=NewRequest,
                  status_code=status.HTTP_201_CREATED)
async def new_request(db: db_dependency, user: user_dependency,
                      new_request: NewRequest = Depends()):

    return new_request_logic(db, user, new_request)
    


@auth_router.post("/newquote", status_code=status.HTTP_201_CREATED,
                  response_model=ViewQuote)
async def new_quote(db: db_dependency, user: user_dependency,
                    new_quote_data: NewQuote = Depends()):
    return new_quote_logic(db, user, new_quote_data)



"""
    the user can update the status of the quote submitted
    by the mechanic to accepted or declined - default is pending
"""


@auth_router.put("/quote/status", response_model=ViewQuote)
async def accept_or_decline_quote(db: db_dependency, user: user_dependency,
                                  status_update: AcceptOrDecline= Depends()):
    accept_or_decline_quote_logic(db, user, status_update)


# return all requests related to the user or mechanic
@auth_router.get("/myrequests", response_model=list[ViewRequest])
async def my_requests(db: db_dependency, user: user_dependency):
    return my_requests_logic(db, user)


# return all the quotes related to the user or mechanic
@auth_router.get("/myquotes", response_model=list[ViewQuote])
async def my_quotes(db: db_dependency, user: user_dependency):
    return my_requests_logic(db, user)


"""
    deleting requests submited by the current user,
    users cant delete other users requests by mistake
"""
@auth_router.delete("/deleterequest/{request_id}")
async def delete_request(request_id: int, db: db_dependency,
                         user: user_dependency):
    delete_request_logic(request_id, db, user)


"""
    deleting quotes submited by the current user - mechanic,
    mechanics cant delete other mechanics quotes by mistake
"""
@auth_router.delete("/deletequote/{quote_id}")
async def delete_quote(quote_id: int, db: db_dependency,
                       user: user_dependency):
    delete_quote_logic(quote_id, db, user)


@auth_router.patch("/profile/edit", response_model=ViewUser)
async def edit_user_profile(db: db_dependency,
                            user: user_dependency, edit_data: EditUser = Depends()):
    return edit_user_profile_logic(db, user, edit_data)


@auth_router.patch("/mechanic/profile/edit", response_model=ViewMechanic)
async def edit_mechanic_profile(db: db_dependency,
                                user: user_dependency, edit_data: EditMechanic = Depends()):
    return edit_mechanic_profile_logic(db, user, edit_data)
    
