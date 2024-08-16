from typing import Optional, Annotated, List, Type
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from pydantic import BaseModel, Field
from ..models import Movie, Users
from ..database import sessionLocal
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class MovieRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed to create', default=None)
    title: str = Field(min_length=2)
    director: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1888, le=2400)
    rating: int = Field(ge=0, le=10)
    comment: str

    class CommentCreate(BaseModel):
        content: str
        parent_id: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Matrix",
                "director": "John Wick",
                "description": "Revenge",
                "category": "Action",
                "year": "2024",
                "rating": 9,
                "comment": "Interesting Movie"

            }
        }
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_movies(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Movie).filter(Movie.owner_id == user.get('id')).all()


@router.get("/MovieApp/{movie_title}", response_model=MovieRequest, status_code=status.HTTP_200_OK)
async def read_movie(movie_title: str, db: db_dependency):
    movie = db.query(Movie).filter(Movie.title == movie_title).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.get("/MovieApp/by_rating/", response_model=List[MovieRequest])
async def read_movie_by_rating(movie_rating: int, db: db_dependency):
    return db.query(Movie).filter(Movie.rating == movie_rating).all()


@router.get("/MovieApp/by_category/", response_model=List[MovieRequest])
async def read_movie_by_category(category: str, db: db_dependency):
    return db.query(Movie).filter(Movie.category == category).all()


@router.get("/MovieApp/bydirector/{director}", response_model=List[MovieRequest])
async def read_movies_by_director_path(director: str, db: db_dependency):
    return db.query(Movie).filter(Movie.director == director).all()


@router.get("/MovieApp/by_year/", response_model=List[MovieRequest])
async def read_movies_by_year(year: int, db: db_dependency):
    return db.query(Movie).filter(Movie.year == year).all()


@router.post("/MovieApp/", response_model=MovieRequest, status_code=status.HTTP_201_CREATED)
async def create_movie(user: user_dependency, movie_request: MovieRequest,
                       db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    owner_id = user.get('id')
    if owner_id is None:
        raise HTTPException(status_code=400, detail='User ID not found')

    db_movie = Movie(
        title=movie_request.title,
        director=movie_request.director,
        description=movie_request.description,
        category=movie_request.category,
        year=movie_request.year,
        rating=movie_request.rating,
        comment=movie_request.comment,
        owner_id=owner_id
    )

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.put("/MovieApp/{movie_title}/", response_model=MovieRequest)
async def update_movie(user: user_dependency, movie_title: str, movie_request: MovieRequest, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    movie = db.query(Movie).filter(Movie.title == movie_title) \
        .filter(Movie.owner_id == user.get('id')).first()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie_request.dict().items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/MovieApp/{movie_title}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(user: user_dependency, movie_title: str, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    movie = db.query(Movie).filter(Movie.title == movie_title) \
        .filter(Movie.owner_id == user.get('id')).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.query(Movie).filter(Movie.title == movie_title) \
        .filter(Movie.owner_id == user.get('id')).delete()

    db.delete(movie)

    db.commit()
    return {"message": "Movie deleted successfully"}
