from fastapi import Body, FastAPI

app = FastAPI()

MOVIES = [
    {"title": "The Shawshank Redemption", "author": "Frank Darabont", "category": "Drama", "year": 1994},
    {"title": "The Godfather", "author": "Francis Ford Coppola", "category": "Crime", "year": 1972},
    {"title": "The Dark Knight", "author": "Christopher Nolan", "category": "Action", "year": 2008},
    {"title": "The Lord of the Rings: The Return of the King", "author": "Peter Jackson", "category": "Adventure",
     "year": 2003},
    {"title": "Pulp Fiction", "author": "Quentin Tarantino", "category": "Crime", "year": 1994},
    {"title": "Schindler's List", "author": "Steven Spielberg", "category": "Drama", "year": 1993},
    {"title": "12 Angry Men", "author": "Sidney Lumet", "category": "Drama", "year": 1957},
    {"title": "The Good, the Bad and the Ugly", "author": "Sergio Leone", "category": "Western", "year": 1966},
    {"title": "The Matrix", "author": "Wachowski siblings", "category": "Sci-Fi", "year": 1999},
    {"title": "Inception", "author": "Christopher Nolan", "category": "Sci-Fi", "year": 2010},
    {"title": "The Godfather Part II", "author": "Francis Ford Coppola", "category": "Crime", "year": 1974},
    {"title": "The Dark Knight Rises", "author": "Christopher Nolan", "category": "Action", "year": 2012},
    {"title": "Memento", "author": "Christopher Nolan", "category": "Thriller", "year": 2000},
    {"title": "Pulp Fiction", "author": "Quentin Tarantino", "category": "Crime", "year": 1994},
    {"title": "Jurassic Park", "author": "Steven Spielberg", "category": "Sci-Fi", "year": 1993}
]


@app.get("/MovieApp")
async def read_all_movies():
    return MOVIES


@app.get("/MovieApp/{movie_title}")
async def read_movies(movie_title: str):
    for movie in MOVIES:
        if movie.get('title').casefold() == movie_title.casefold():
            return movie


@app.get("/MovieApp/by_category/")
async def read_movie_by_category(category: str):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get('category').casefold() == category.casefold():
            movies_to_return.append(movie)
    return movies_to_return

@app.get("/MovieApp/byauthor/{author}")
async def read_movies_by_author_path(author:str):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get("author").casefold() == author.casefold():
            movies_to_return.append(movie)
    return movies_to_return

@app.get("/MovieApp/by_year/")
async def read_movies_by_year(year: int):
    movies_to_return = []
    for movie in MOVIES:
        if movie.get('year') == year:
            movies_to_return.append(movie)
    return movies_to_return


@app.post("/MovieApp/create_movie/")
async def create_movie(new_movie=Body()):
    MOVIES.append(new_movie)


@app.put("/MovieApp/update_movie/")
async def update_movie(updated_movie=Body()):
    for i in range(len(MOVIES)):
        if MOVIES[i].get("title").casefold() == updated_movie.get("title").casefold():
            MOVIES[i] = updated_movie


@app.delete("/MovieApp/delete_movie/{movie_title}")
async def delete_movie(movie_title: str):
    for i in range(len(MOVIES)):
        if MOVIES[i].get("title").casefold() == movie_title.casefold():
            MOVIES.pop(i)
            break
