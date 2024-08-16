from typing import Optional, Annotated, List, Type
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from pydantic import BaseModel, Field
from MovieApp.models import Movie, Users, Comment
from MovieApp.database import sessionLocal
from sqlalchemy.orm import Session
from starlette import status
from MovieApp.auth import get_current_user
router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    content: str
    title: str
    movie_id: int
    user_id: int
    parent_id: Optional[int]
    replies: List['CommentResponse'] = []

    class Config:
        orm_mode = True


@router.post("/MovieApp/{movie_title}/comments/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(movie_title: str, comment: CommentCreate, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    movie = db.query(Movie).filter(Movie.title == movie_title).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_comment = Comment(content=comment.content, movie_title=movie_title, user_id=user.id, parent_id=comment.parent_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/MovieApp/{movie_title}/comments/", response_model=List[CommentResponse])
async def read_comments(movie_title: str, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.movie_title == movie_title).all()
    return comments

