from fastapi import FastAPI

from db import models
from db.database import engine

from routers import user, account
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(account.router)

@app.get('/')
def index():
    return {'health' : 'works'}

models.Base.metadata.create_all(engine)