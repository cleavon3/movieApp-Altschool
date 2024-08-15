from fastapi import status
from ..routers.movies import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_movie():
    movie = Movie(
        id=1,
        title='Matrix',
        director='John Wick',
        description='Revenge',
        category='Action',
        year=2024,
        rating=9,
        comment='Interesting Movie',
        complete=False,
    )

    db = TestingSessionLocal()
    db.add(movie)
    db.commit()
    yield movie
    with engine.connect() as connection:
        connection.execute(text("DELETE from movies;"))
        connection.commit()


def test_read_all_authenticated(test_movie):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Matrix', 'id': 1, 'director': 'John Wick',
                                'description': 'Revenge', 'category': 'Action', 'year': 2024,
                                'rating': 9, 'comment': 'Interesting Movie', 'owner_id': 1}]


def test_create_movie(test_movie):
    request_data = {
        #'id': 1,
        'title': 'Matrix',
        'director': 'John Wick',
        'description': 'Revenge',
        'category': 'Action',
        'year': 2024,
        'rating': 9,
        'comment': 'Interesting Movie',
        'complete': False,
       # 'owner_id': 1
    }

    response = client.post('/MovieApp/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Movie).filter(Movie.title == 'Matrix').first()
    assert model.title == request_data.get('title')
    assert model.director == request_data.get('director')
    assert model.description == request_data.get('description')
    assert model.category == request_data.get('category')
    assert model.year == request_data.get('year')
    assert model.rating == request_data.get('rating')
    assert model.comment == request_data.get('comment')
    assert model.complete == request_data.get('complete')

    def test_update_movie(test_movie):
        movie_title = 'Matrix'
        request_data = {
            'title': 'Matrix',
            'director': 'John Wick',
            'description': 'Revenge Updated',
            'category': 'Action',
            'year': 2024,
            'rating': 9,
            'comment': 'Updated Comment',
            'complete': True
        }

        response = client.put(f'/MovieApp/{movie_title}/', json=request_data)
        assert response.status_code == 200

        db = TestingSessionLocal()
        model = db.query(Movie).filter(Movie.title == request_data['title']).first()
        assert model is not None
    # Assert that the movie was updated correctly
    assert model.title == request_data.get('title')
    assert model.director == request_data.get('director')
    assert model.description == request_data.get('description')
    assert model.category == request_data.get('category')
    assert model.year == request_data.get('year')
    assert model.rating == request_data.get('rating')
    assert model.comment == request_data.get('comment')
    assert model.complete == request_data.get('complete')


def test_update_movie_not_found(test_movie):

    request_data = {
        #'id': 1,
        'title': 'Matrix',
        'director': 'John Wick',
        'description': 'Revenge',
        'category': 'Action',
        'year': 2024,
        'rating': 9,
        'comment': 'Interesting Movie',
        'complete': False,
        #'owner_id': 1
    }

    response = client.put(f'/MovieApp/NonExistentMovie/', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Movie not found'}

def test_delete_movie(test_movie):
    movie_title = 'Matrix'

    response = client.delete(f'/MovieApp/{movie_title}/')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Movie).filter(Movie.title == movie_title).first()
    assert model is None


def test_delete_movie_not_found():
    movie_title = 'NonExistentMovie'

    response = client.delete(f'/MovieApp/{movie_title}/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Movie not found'}
