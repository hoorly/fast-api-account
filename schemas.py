from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import datetime

class UserBase(BaseModel):
    id: int
    username: str
    email: str
    password: str

class AccountInUser(BaseModel):
    id: int
    balance: Decimal
    class Config():
        orm_mode = True

class UserDisplay(BaseModel):
    username: str
    email: str
    accounts: List[AccountInUser] = []
    class Config():
        orm_mode = True

class AccountBase(BaseModel):
    id: int
    balance: Decimal
    created: datetime
    last_access: datetime
    user_id: int
    class Config():
        orm_mode = True

class AccountDisplay(BaseModel):
    balance: Decimal
    #user_id: int
    class Config():
        orm_mode = True

