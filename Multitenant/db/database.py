from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/multitenant"



#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/multitenant_testing_database"




engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
session = SessionLocal()
Base = declarative_base()


