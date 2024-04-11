from sqlalchemy import Column, DateTime, Boolean, event, Integer, String
from datetime import datetime

from .base import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


@event.listens_for(Base, 'before_update')
@event.listens_for(Base, 'before_insert')
def timestamp_before_update(mapper, connection, target):
    target.updated_at = datetime.utcnow()


class BaseModel(Base, TimestampMixin):
    __abstract__ = True


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
