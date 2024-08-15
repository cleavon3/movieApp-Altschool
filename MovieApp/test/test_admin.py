from fastapi import status
from ..models import Movie
from .utils import *
from ..routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_real_all_authenticate(test_movie):
    response = client.get("/admin/MovieApp")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Matrix', 'id': 1, 'director': 'John Wick',
                                'description': 'Revenge', 'category': 'Action', 'year': 2024,
                                'rating': 9, 'comment': 'Interesting Movie', 'owner_id': 1}]


def test_admin_delete_movie(test_movie):
    # Replace 'Matrix' with the actual title of the movie you want to delete
    response = client.delete("admin/MovieApp/Matrix")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Movie).filter(Movie.title == 'Matrix').first()
    assert model is None


def test_admin_delete_movie_not_found():
    response = client.delete("admin/MovieApp/Matrices")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Movie not found'}
