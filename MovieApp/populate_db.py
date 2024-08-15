from sqlalchemy.orm import Session
from database import engine, sessionLocal
import models

db = sessionLocal()
# List of movies to add to the database
MOVIES = [
    {"Title": "The Shawshank Redemption", "director": "Frank Darabont", "description": "A banker wrongly imprisoned for the murder of his wife and her lover starts a long friendship with a cellmate and finds a way to escape.", "category": "Drama", "year": 1994, "rating": 9, "comment": "A masterpiece of storytelling"},
    {"Title": "The Godfather", "director": "Francis Ford Coppola", "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "category": "Crime", "year": 1972, "rating": 9, "comment": "Iconic cinematic experience"},
    {"Title": "The Dark Knight", "director": "Christopher Nolan", "description": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.", "category": "Action", "year": 2008, "rating": 9, "comment": "Thrilling and intense"},
    {"Title": "Pulp Fiction", "director": "Quentin Tarantino", "description": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "category": "Crime", "year": 1994, "rating": 8, "comment": "Bold and original"},
    {"Title": "The Lord of the Rings: The Return of the King", "director": "Peter Jackson", "description": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.", "category": "Fantasy", "year": 2003, "rating": 8, "comment": "Epic and visually stunning"},
    {"Title": "Forrest Gump", "director": "Robert Zemeckis", "description": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.", "category": "Drama", "year": 1994, "rating": 7, "comment": "Heartwarming and emotional"},
    {"Title": "Inception", "director": "Christopher Nolan", "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.", "category": "Sci-Fi", "year": 2010, "rating": 6, "comment": "Mind-bending and innovative"},
    {"Title": "Fight Club", "director": "David Fincher", "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "category": "Drama", "year": 1999, "rating": 7, "comment": "Dark and thought-provoking"},
    {"Title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "category": "Sci-Fi", "year": 1999, "rating": 9, "comment": "Revolutionary and thrilling"},
    {"Title": "Goodfellas", "director": "Martin Scorsese", "description": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.", "category": "Crime", "year": 1990, "rating": 6, "comment": "Gripping and realistic"},
    {"Title": "The Silence of the Lambs", "director": "Jonathan Demme", "description": "A young FBI cadet must confide in an incarcerated and manipulative killer to receive his help on catching another serial killer who skins his victims.", "category": "Thriller", "year": 1991, "rating": 7, "comment": "Chilling and suspenseful"},
    {"Title": "Se7en", "director": "David Fincher", "description": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.", "category": "Crime", "year": 1995, "rating": 8, "comment": "Dark and disturbing"},
    {"Title": "The Usual Suspects", "director": "Bryan Singer", "description": "A sole survivor tells a riveting story of a heist gone wrong and the mysterious figure known as Keyser Söze.", "category": "Crime", "year": 1995, "rating": 8, "comment": "Cunning and unpredictable"},
    {"Title": "The Departed", "director": "Martin Scorsese", "description": "An undercover cop and a mole in the police force try to identify each other while infiltrating an Irish gang in Boston.", "category": "Crime", "year": 2006, "rating": 9, "comment": "Tense and well-crafted"},
    {"Title": "The Green Mile", "director": "Frank Darabont", "description": "A supernatural tale set on death row where a corrections officer discovers that one of his inmates has a miraculous gift.", "category": "Drama", "year": 1999, "rating": 9, "comment": "Emotional and touching"},
    {"Title": "The Prestige", "director": "Christopher Nolan", "description": "Two stage magicians engage in a competitive rivalry, creating elaborate illusions and tricks, with dire consequences.", "category": "Drama", "year": 2006, "rating": 7, "comment": "Clever and intricate"},
    {"Title": "Interstellar", "director": "Christopher Nolan", "description": "A group of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "category": "Sci-Fi", "year": 2014, "rating": 8, "comment": "Visually stunning and thought-provoking"}
]

# Create the database and the database table
models.Base.metadata.create_all(bind=engine)

# Create a new session
db: Session = sessionLocal()

# Add all movies to the session
for movie in MOVIES:
    db_movie = models.Movie(**movie)
    db.add(db_movie)

# Commit the session to the database
db.commit()

# Close the session
db.close()

print("Database populated successfully.")
