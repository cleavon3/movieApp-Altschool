from fastapi import FastAPI
from MovieApp.models import Base
from MovieApp.database import engine
from MovieApp.routers import auth, movies, admin, users, comment


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(comment.router)
