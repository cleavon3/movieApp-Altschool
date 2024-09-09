from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:composition@localhost:5432/MovieAppDatabase"
#SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:composition@localhost:5432/MovieAppDatabase"
#SQLALCHEMY_DATABASE_URL = "postgresql://username:composition@localhost:5432/MovieAppDatabase"
#SQLALCHEMY_DATABASE_URL = "postgresql://your_username:your_password@localhost:5432/your_database_name"




engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



