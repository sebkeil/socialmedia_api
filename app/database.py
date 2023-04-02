"""
Make connection to database via sqlalchemy ORM (rather than db drivers directly)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = 'postgresql://postgres:pAlcacer9!@localhost/socialmedia_api'

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# create database dependency (code from FastAPI documentation)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

