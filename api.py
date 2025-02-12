import os, requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie/{}"

def fetch_movie_data(movie_name):
    params = {"api_key": TMDB_API_KEY, "query": movie_name}
    search_resp = requests.get(TMDB_SEARCH_URL, params=params)
    if search_resp.status_code != 200:
        raise ValueError("Error connecting to TMDB API.")
    results = search_resp.json().get("results")
    if not results:
        raise ValueError(f"Movie '{movie_name}' not found on TMDB.")
    
    movie_id = results[0]["id"]
    title = results[0]["title"]
    details_resp = requests.get(TMDB_DETAILS_URL.format(movie_id), params={"api_key": TMDB_API_KEY})
    if details_resp.status_code != 200:
        raise ValueError("Error fetching movie details from TMDB.")
    details = details_resp.json()
    summary = details.get("overview")
    genres = [g["name"] for g in details.get("genres", [])]
    if not summary:
        raise ValueError("No summary found for this movie.")
    
    return {"title": title, "summary": summary, "genres": genres}
