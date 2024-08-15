from typing import Optional, Annotated, List, Type
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from pydantic import BaseModel, Field
from ..models import Movie, Users
from ..database import sessionLocal
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]




@router.get("/MovieApp", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Movie).all()


@router.delete("/MovieApp/{movie_title}", status_code=status.HTTP_204_NO_CONTENT)
async  def delete_movie(user: user_dependency, db: db_dependency, movie_title:str):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    movie = db.query(Movie).filter(Movie.title == movie_title).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found,')

    db.query(Movie).filter(Movie.title == movie_title).delete()

    db.commit()

