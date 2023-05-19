from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import AccountBase, AccountDisplay, UserBase
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_account
from auth.oauth2 import oauth2_scheme, get_current_user

router = APIRouter(
    prefix='/account',
    tags=['user','account']
)

@router.post('/', response_model=AccountBase)
def create_account(request: AccountDisplay, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_account.create_account(db, request, current_user)

@router.get('/', response_model=List[AccountBase])
def get_all_accounts(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    accounts = db_account.get_all_accounts(db)
    return accounts

@router.get('/{id}', response_model=AccountBase) # can go by token
def get_account(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    account = db_account.get_account(db, id)
    return account