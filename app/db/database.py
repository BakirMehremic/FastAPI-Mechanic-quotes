from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

DATABASE_URL = settings.db_location

# echo=True
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=settings.db_autoflush,
                            autocommit=settings.db_autocommit, bind=engine)

Base = declarative_base()




        