from fastapi.security import OAuth2PasswordBearer
from db.models import User, Mechanic
from datetime import datetime, timedelta
from core.config import settings
from jose import jwt


bcrypt_context = settings.bcrypt_context
# added schema_name so there are two login fields in swagger for admin and users/mechanics
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token",
                                     scheme_name="oauth2_schema")


def authenticate_user(username: str, password: str, db) -> User | Mechanic | bool:
    user = db.query(User).filter(User.username == username).first()
    mechanic = db.query(Mechanic).filter(Mechanic.username == username).first()
    if (user is None) and (mechanic is None):
        return False

    try:
        user_pw_valid = bcrypt_context.verify(password, user.hashed_password)
        if user_pw_valid:
            return user
    except:
        mechanic_pw_valid = bcrypt_context.verify(password, mechanic.hashed_password)
        if mechanic_pw_valid:
            return mechanic

    return False


# no refresh token for the sake of simplicity
def create_access_token(username: str, user_id: int) -> str:
    encode = {"sub": username, "id": user_id}  # the jwt contains the username and user_id
    expires = datetime.now() + timedelta(minutes=settings.expires_delta)
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
