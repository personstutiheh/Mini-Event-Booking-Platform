import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL") #reads the variable loaded
engine = create_engine(DATABASE_URL) #connection pool, creats sqlalchemy engine

#query for data, add or update records, commit or rollback transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#to manage the lifecycle of a db sesh
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
