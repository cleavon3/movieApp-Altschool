from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Movie:
    id: int
    title: str
    director: str
    description: str
    category: str
    year: int
    rating: int
    comment: str

    def __init__(self, id, title, director, category, year, description, rating, comment):
        self.id = id
        self.title = title
        self.director = director
        self.category = category
        self.year = year
        self.description = description
        self.rating = rating
        self.comment = comment


class MovieRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed to create', default=None)
    title: str = Field(min_length=2)
    director: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1888, le=2400)
    rating: int = Field(ge=0, le=11)
    comment: str

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


MOVIES = [

    Movie(1, "The Shawshank Redemption", "Frank Darabont", "Drama", 1994,
          "A banker wrongly imprisoned for the murder of his wife and her lover starts a long friendship with a cellmate and finds a way to escape.",
          9, "A masterpiece of storytelling"),

    Movie(2, "The Godfather", "Francis Ford Coppola", "Crime", 1972,
          "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
          9, "Iconic cinematic experience"),

    Movie(3, "The Dark Knight", "Christopher Nolan", "Action", 2008,
          "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
          9, "Thrilling and intense"),

    Movie(4, "Pulp Fiction", "Quentin Tarantino", "Crime", 1994,
          "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
          8, "Bold and original"),

    Movie(5, "The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantasy", 2003,
          "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
          8, "Epic and visually stunning"),

    Movie(6, "Forrest Gump", "Robert Zemeckis", "Drama", 1994,
          "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
          7, "Heartwarming and emotional"),

    Movie(7, "Inception", "Christopher Nolan", "Sci-Fi", 2010,
          "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.",
          6, "Mind-bending and innovative"),

    Movie(8, "Fight Club", "David Fincher", "Drama", 1999,
          "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
          7, "Dark and thought-provoking"),

    Movie(9, "The Matrix", "Lana Wachowski, Lilly Wachowski", "Sci-Fi", 1999,
          "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
          9, "Revolutionary and thrilling"),

    Movie(10, "Goodfellas", "Martin Scorsese", "Crime", 1990,
          "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.",
          6, "Gripping and realistic"),

    Movie(11, "The Silence of the Lambs", "Jonathan Demme", "Thriller", 1991,
          "A young FBI cadet must confide in an incarcerated and manipulative killer to receive his help on catching another serial killer who skins his victims.",
          7, "Chilling and suspenseful"),

    Movie(12, "Se7en", "David Fincher", "Crime", 1995,
          "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
          8, "Dark and disturbing"),

    Movie(13, "The Usual Suspects", "Bryan Singer", "Crime", 1995,
          "A sole survivor tells a riveting story of a heist gone wrong and the mysterious figure known as Keyser Söze.",
          8, "Cunning and unpredictable"),

    Movie(14, "The Departed", "Martin Scorsese", "Crime", 2006,
          "An undercover cop and a mole in the police force try to identify each other while infiltrating an Irish gang in Boston.",
          9, "Tense and well-crafted"),

    Movie(15, "The Green Mile", "Frank Darabont", "Drama", 1999,
          "A supernatural tale set on death row where a corrections officer discovers that one of his inmates has a miraculous gift.",
          9, "Emotional and touching"),

    Movie(16, "The Prestige", "Christopher Nolan", "Drama", 2006,
          "Two stage magicians engage in a competitive rivalry, creating elaborate illusions and tricks, with dire consequences.",
          7, "Clever and intricate"),

    Movie(17, "Interstellar", "Christopher Nolan", "Sci-Fi", 2014,
          "A group of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
          8, "Visually stunning and thought-provoking")
]


@app.get("/MovieApp/")
async def read_all_movies():
    return MOVIES


@app.get("/MovieApp/{movie_title}")
async def read_movie(movie_title: str = Path(min_length=2)):
    for movie in MOVIES:
        if movie.title.casefold() == movie_title.casefold():
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get("/MovieApp/by_rating/")
async def read_movie_by_rating(movie_rating: int = Query(ge=0, le=11)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.rating == movie_rating:
            movies_to_return.append(movie)
    return movies_to_return


@app.get("/MovieApp/by_category/")
async def read_movie_by_category(category: str = Query(min_length=1, max_length=50)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.category.casefold() == category.casefold():
            movies_to_return.append(movie)
    return movies_to_return


@app.get("/MovieApp/bydirector/{director}")
async def read_movies_by_director_path(director: str = Path(min_length=1)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.director.casefold() == director.casefold():
            movies_to_return.append(movie)
    return movies_to_return


@app.get("/MovieApp/by_year/")
async def read_movies_by_year(year: int = Query(ge=1888, le=2400)):
    movies_to_return = []
    for movie in MOVIES:
        if movie.year == year:
            movies_to_return.append(movie)
    return movies_to_return


@app.put("/MovieApp/update_movie/")
async def update_movie(movie: MovieRequest):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].title == movie.title:
            MOVIES[i] = movie
            movie_changed = True
            return {"message": "Movie updated successfully"}
    if not movie_changed:
        raise HTTPException(status_code=404, detail="Movie not found")

@app.post("/create_movie/")
async def create_movie(movie_request: MovieRequest):
    new_movie = Movie(**movie_request.dict())
    MOVIES.append(new_movie)
    return {"message": "Movie created successfully"}


@app.delete("/MovieApp/{movie_title}/")
async def delete_movie(movie_title: str = Path(min_length=2)):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].title.casefold() == movie_title.casefold():
            MOVIES.pop(i)
            movie_changed = True
            return {"message": "Movie deleted successfully"}
    if not movie_changed:
        raise HTTPException(status_code=404, detail="Movie not found")


