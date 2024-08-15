from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from ..routers.auth import bcrypt_context
from ..models import Movie, Users
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:composition@localhost/MovieAppDatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'cleavontest', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_user():
    user = Users(
        email='cleavon@gmail.com',
        first_name='ESE',
        username='cleavontest',
        hashed_password=bcrypt_context.hash('testpassword'),
        role='admin',
        phone_number='0000654934089',
        id=1
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users'))
        connection.commit()

@pytest.fixture
def test_movie(test_user):
    movie = Movie(
        title='Matrix',
        director='John Wick',
        description='Revenge',
        category='Action',
        year=2024,
        rating=9,
        comment='Interesting Movie',
        complete=False,
        owner_id=test_user.id  # Use valid owner_id
    )

    db = TestingSessionLocal()
    db.add(movie)
    db.commit()
    yield movie
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM movies"))
        connection.commit()
