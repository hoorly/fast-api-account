from db.database import Base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, DECIMAL, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    accounts = relationship('DbAccount', back_populates='user')

class DbAccount(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(DECIMAL(10,2))
    created = Column(DateTime(timezone=True), server_default=func.now())
    last_access = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('DbUser', back_populates='accounts')