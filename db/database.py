from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

SQLALCHEMY_DATABASE_URL = "sqlite:///data/accounts.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

rediska = redis.Redis(host='redis', port=6379)
try:
    rediska.ping()
except:
    rediska = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
