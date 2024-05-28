from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from dependencies import db_dependency, user_dependency
from db.models import Request, Quote
from fastapi.security import OAuth2PasswordRequestForm
from db.schemas import (NewRequest, NewQuote, AcceptOrDecline,
                        EditMechanic, EditUser)
from services.users_auth import authenticate_user, create_access_token
from utils import is_user, get_current_user_obj

"""
    all the routes logic which require user authentification
    are in this file, the logic is in services.user_auth

    the authorization is done in the way fastapi recommends
"""


# returns jwt tokens for both users and mechanics
def login_for_access_token_logic(db: db_dependency,
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong username or password")

    if hasattr(user, "user_id"):
        token = create_access_token(user.username, user.user_id)
    else:
        token = create_access_token(user.username, user.mechanic_id)

    return {"access_token": token, "token_type": "bearer"}


def new_request_logic(db: db_dependency, user: user_dependency,
                      new_request: NewRequest = Depends()):
    if not is_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Mechanics can not place requests")

    """
    new order request takes:
    mechanic_id: int 
    car: str 
    description: Optional[str]"""
    new_request = Request(
        user_id=user.get("id"),
        mechanic_id=new_request.mechanic_id,
        car=new_request.car
    )

    if new_request.description:
        new_request.description = new_request.description

    db.add(new_request)
    db.commit()

    return new_request


def new_quote_logic(db: db_dependency, user: user_dependency,
                    new_quote_data: NewQuote = Depends()):
    if is_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only mechanics can send quotes")

    current_user = get_current_user_obj(current_user=user, db=db)

    # works for checking both if the request exists and if it is addresed to the current user
    my_requests = [request.request_id for request in current_user.requests]
    if new_quote_data.request_id not in my_requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no request for a quote under this id")

    quote_exists = db.query(Quote).join(Request).filter(
        Quote.request_id == new_quote_data.request_id,
        Request.mechanic_id == current_user.mechanic_id).first()

    if quote_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You already sent a quote for this request")

    new_quote = Quote(
        request_id=new_quote_data.request_id,
        amount=new_quote_data.amount
    )

    if new_quote_data.description:
        new_quote.description = new_quote_data.description

    db.add(new_quote)
    db.commit()

    return new_quote


"""
    the user can update the status of the quote submitted
    by the mechanic to accepted or declined - default is pending
"""


def accept_or_decline_quote_logic(db: db_dependency, user: user_dependency,
                                  status_update: AcceptOrDecline = Depends()):
    if not is_user(current_user=user, db=db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Only users can update the status")

    current_user = get_current_user_obj(current_user=user, db=db)

    # checks if it exists and if it is submited by the current user
    quote = db.query(Quote).join(Request).filter(
        Quote.quote_id == status_update.quote_id,
        Request.user_id == current_user.user_id
    ).first()

    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No quote with this id")

    quote.status = status_update.status
    db.commit()

    return quote


# return all requests related to the user or mechanic
def my_requests_logic(db: db_dependency, user: user_dependency):
    current_user = get_current_user_obj(current_user=user, db=db)
    if not current_user.requests:
        raise HTTPException(status_code=404,
                            detail="You have no requests")
    return current_user.requests


# return all the quotes related to the user or mechanic
def my_quotes_logic(db: db_dependency, user: user_dependency):
    current_user = get_current_user_obj(current_user=user, db=db)

    if is_user(user, db):
        requests = db.query(Request).filter(Request.user_id == current_user.user_id).all()
    else:
        requests = db.query(Request).filter(Request.mechanic_id == current_user.mechanic_id).all()

    if not requests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="You have no quotes")

    quotes = list()

    for request in requests:
        quotes.extend(request.quotes)

    return quotes


"""
    deleting requests submited by the current user,
    users cant delete other users requests by mistake
"""


def delete_request_logic(request_id: int, db: db_dependency,
                         user: user_dependency):
    if not is_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Mechanics cant delete requests")

    current_user = get_current_user_obj(user, db)

    to_delete = db.query(Request).filter(Request.request_id == request_id).first()
    if to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No request under this id")

    for request in current_user.requests:
        if request.request_id == request_id:
            db.delete(request)
            db.commit()
            return {"deleted request with id:": request_id}


"""
    deleting quotes submited by the current user - mechanic,
    mechanics cant delete other mechanics quotes by mistake
"""


def delete_quote_logic(quote_id: int, db: db_dependency,
                       user: user_dependency):
    if is_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Users cant delete quotes")

    current_user = get_current_user_obj(user, db)

    requests = db.query(Request).filter(Request.mechanic_id == current_user.mechanic_id).all()

    quotes = list()

    for request in requests:
        quotes.extend(request.quotes)

    for quote in quotes:
        if quote.quote_id == quote_id:
            db.delete(quote)
            db.commit()
            return {"deleted quote with id:": quote_id}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No quote under this id")


def edit_user_profile_logic(db: db_dependency,
                            user: user_dependency, edit_data: EditUser = Depends()):
    if not is_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Route limited to users")

    current_user = get_current_user_obj(user, db)

    if edit_data.name:
        current_user.name = edit_data.name
    if edit_data.contact_number:
        current_user.contact_number = edit_data.contact_number

    db.commit()

    return current_user


async def edit_mechanic_profile_logic(db: db_dependency,
                                      user: user_dependency, edit_data: EditMechanic = Depends()):
    if is_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Route limited to mechanics")

    current_user = get_current_user_obj(user, db)

    if edit_data.workshop:
        current_user.workshop = edit_data.workshop
    if edit_data.contact_number:
        current_user.contact_number = edit_data.contact_number
    if edit_data.address:
        current_user.address = edit_data.address

    db.commit()

    return current_user
