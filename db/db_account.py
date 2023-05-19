from sqlalchemy.orm.session import Session
from schemas import AccountDisplay, UserBase
from db.models import DbAccount
from fastapi import HTTPException, status
from db.database import rediska

def create_account(db: Session, request: AccountDisplay, user: UserBase):
    new_account = DbAccount(
        balance = request.balance,
        user_id = user.id
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def get_all_accounts(db: Session):
    accounts = db.query(DbAccount).all()
    if not accounts or len(accounts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No accounts found')
    return accounts

def get_all_user_accounts(db: Session, user: UserBase):
    accounts = db.query(DbAccount).filter(DbAccount.user_id == user.id)
    if not accounts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No accounts found')
    return accounts

def get_account(db: Session, id: int):
    account = db.query(DbAccount).filter(DbAccount.id == id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Account with id {id} not found')
    return account