import json
import os
from config import config

JSON_PATH = config.get("JSON_PATH")

def load_preloaded_movies(json_path=JSON_PATH):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, json_path)
    
    with open(file_path, "r", encoding="utf-8") as f:
        movies = json.load(f)
    return movies

# Optionally, load thumbnails as a list if needed
def load_thumbnails(json_path=JSON_PATH):
    movies = load_preloaded_movies(json_path)
    thumbnails = [movie.get("thumbnail") for movie in movies if movie.get("thumbnail")]
    return thumbnails

# You can export the loaded data for use in other modules:
preloaded_movies = load_preloaded_movies()
thumbnails = load_thumbnails()
