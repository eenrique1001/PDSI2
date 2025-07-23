from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
"""""
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

"""
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

#print("Using DB URL:", SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker( autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()