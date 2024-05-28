from fastapi.security import OAuth2PasswordBearer
from db.models import Admin
from datetime import datetime, timedelta
from jose import jwt
from core.config import settings


bcrypt_context = settings.bcrypt_context
# added schema_name so there are two login fields in swagger for admin and users/mechanics
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="admin/token",
                                     scheme_name="admin_oauth2_schema")


def authenticate_user(username: str, password: str, db) -> Admin | bool:
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None:
        return False

    admin_pw_valid = bcrypt_context.verify(password, admin.hashed_password)
    if admin_pw_valid:
        return admin

    return False


# no refresh token for the sake of simplicity
def create_access_token(username: str, admin_id: int) -> str:
    encode = {"sub": username, "id": admin_id}  # the jwt contains the username and user_id
    expires = datetime.now() + timedelta(minutes=settings.expires_delta)
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



