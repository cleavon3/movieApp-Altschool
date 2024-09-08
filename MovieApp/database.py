from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:composition@localhost/MovieAppDatabase'
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:composition@localhost:5432/MovieAppDatabase"



engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



