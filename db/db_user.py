from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from schemas import UserBase
from db.models import DbUser
from .hash import Hash
from db.database import rediska
import json

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    users = db.query(DbUser).all()
    if not users or len(users) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user found')
    if rediska:
        for user in users:
            key = '%s_%s' % ('user', user.id)
            rediska.set(key, json.dumps({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password
                })
            )
    return users

def get_user(db: Session, id: int):
    if rediska:
        key = '%s_%s' % ('user', id)
        if rediska.exists(key):
            user = json.loads(rediska.get(key))
            return {'id' : user['id'], 'username': user['username'], 'email': user['email'], 'password': user['password']}
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with username {username} not found')
    return user