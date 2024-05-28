from jose import jwt, JWTError
from fastapi import status, HTTPException, Depends
from services.admin_auth import oauth2_bearer as admin_bearer
from services.users_auth import oauth2_bearer as user_bearer
from core.config import settings
from db.models import Admin, User, Mechanic, AdminPermissions
from sqlalchemy.orm import Session
from typing import Annotated


# Function to get the current admin
async def get_current_admin(token: Annotated[str, Depends(admin_bearer)]) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        admin_id: str = payload.get("id")
        if username is None or admin_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate admin")
        return {"username": username, "id": admin_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate admin")


# get the current user
async def get_current_user(token: Annotated[str, Depends(user_bearer)]) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user")


# checking if the current admin has all or partial permissions
def has_permissions(current_admin: dict, db: Session) -> bool:
    admin = db.query(Admin).filter(Admin.username == current_admin.get("username")).first()
    if admin.permissions == AdminPermissions.ALL:
        return True
    return False


# et the current admin object
def get_current_admin_obj(current_admin: dict, db: Session) -> Admin:
    admin = db.query(Admin).filter(Admin.username == current_admin.get("username")).first()
    if admin:
        return admin
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not find user")


# checking if the current user is a user or mechanic
def is_user(current_user: dict, db: Session) -> bool:
    mechanic = db.query(Mechanic).filter(Mechanic.username == current_user.get("username")).first()
    if mechanic:
        return False
    return True


# get the current user object
def get_current_user_obj(current_user: dict, db: Session) -> User | Mechanic:
    user = db.query(User).filter(User.username == current_user.get("username")).first()
    mechanic = db.query(Mechanic).filter(Mechanic.username == current_user.get("username")).first()
    if user:
        return user
    if mechanic:
        return mechanic
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not find user")
