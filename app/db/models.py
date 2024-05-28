from sqlalchemy import (Column, Integer, String,
                        ForeignKey, Text, DateTime, Float, Enum)
from sqlalchemy.orm import relationship
from .database import Base
from .database import engine
from datetime import datetime
import enum

# defining database tables and relationships


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String(50), nullable=False)
    contact_number = Column(Integer)

    requests = relationship("Request", back_populates="user")

    def __repr__(self):
        return f"user id:{self.user_id} username:{self.username}"


class Mechanic(Base):
    __tablename__ = "mechanics"

    mechanic_id = Column(Integer, primary_key=True, autoincrement=True)
    hashed_password = Column(String, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    workshop = Column(String)
    contact_number = Column(Integer, nullable=False)
    address = Column(String)

    requests = relationship("Request", back_populates="mechanic")

    def __repr__(self):
        return f"mechanic id:{self.mechanic_id} name:{self.username}"


class Request(Base):
    __tablename__ = "requests"

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=False)
    car = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now())

    user = relationship("User", back_populates="requests")
    mechanic = relationship("Mechanic", back_populates="requests")
    quotes = relationship("Quote", back_populates="request")


# statuses for the quote which can be changed by the user
class QuoteStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"


class Quote(Base):
    __tablename__ = 'quotes'

    quote_id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.request_id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.PENDING)
    created_at = Column(DateTime, default=lambda: datetime.now())

    request = relationship('Request', back_populates='quotes')


# enum for the admin table, permisions define what they can do
class AdminPermissions(enum.Enum):
    ALL = "all"
    PARTIAL = "partial"
    

class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    permissions = Column(Enum(AdminPermissions), default=AdminPermissions.PARTIAL)
    created_at = Column(DateTime, default=lambda: datetime.now())


User.metadata.create_all(bind=engine)
Mechanic.metadata.create_all(bind=engine)
Request.metadata.create_all(bind=engine)
Quote.metadata.create_all(bind=engine)
Admin.metadata.create_all(bind=engine)


