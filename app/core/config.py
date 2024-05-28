from pydantic_settings import BaseSettings
from passlib.context import CryptContext


class Settings(BaseSettings):
    db_location: str = "sqlite:///../mechanicquotes.db"
    db_autocommit: bool = False
    db_autoflush: bool = False
    enviornment: str = "development"
    SECRET_KEY: str = "2a137ad8b3a46857aa72056150e6da609b0480aa52490892e396fd69b88a2201"
    ALGORITHM: str = "HS256"
    expires_delta: int = 20
    create_admins: bool = True
    bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = Settings()
