import os
import streamlit as st
import numpy as np
import requests
from config import config

from data import preloaded_movies, thumbnails
from api import fetch_movie_data
from models import model, compute_embeddings, create_faiss_index, compute_similarity

STYLESHEET = config.get("STYLE_CSS")

# Utility function to load external CSS from a file.
def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load external CSS (make sure assets/style.css exists)
local_css(STYLESHEET)

# --- Set Up the FAISS Index with Precomputed Embeddings ---
embeddings = compute_embeddings(preloaded_movies, model)
embedding_dim = model.get_sentence_embedding_dimension()
index = create_faiss_index(embeddings, embedding_dim)

# --- Build Marquee HTML for Thumbnails ---
# The styling for these elements is defined in assets/style.css.
left_marquee_html = '<div class="marquee-container marquee-left"><div class="marquee-content">'
for url in thumbnails:
    left_marquee_html += f'<img src="{url}" alt="Thumbnail">'
left_marquee_html += '</div></div>'

right_marquee_html = '<div class="marquee-container marquee-right"><div class="marquee-content">'
for url in thumbnails:
    right_marquee_html += f'<img src="{url}" alt="Thumbnail">'
right_marquee_html += '</div></div>'

# Inject the marquee HTML into the app.
st.markdown(left_marquee_html + right_marquee_html, unsafe_allow_html=True)

# --- Main Streamlit UI ---
st.title("Dynamic Movie Recommendation System")
st.write("Enter the name of a movie to get recommendations based on storyline and genre similarity.")

# Autocomplete input: When the user types at least 3 characters, fetch suggestions from TMDB.
movie_query = st.text_input("Start typing a movie name:")
movie_selected = None
if movie_query and len(movie_query) >= 3:
    tmdb_params = {"api_key": os.getenv("TMDB_API_KEY"), "query": movie_query}
    search_resp = requests.get("https://api.themoviedb.org/3/search/movie", params=tmdb_params)
    if search_resp.status_code == 200:
        results = search_resp.json().get("results", [])
        suggestions = list({result["title"] for result in results})
        if suggestions:
            movie_selected = st.selectbox("Select a movie from suggestions:", suggestions)
        else:
            st.info("No suggestions found.")
    else:
        st.error("Error fetching suggestions from TMDB.")

if not movie_query:
    st.info("Please enter a movie name to get recommendations.")

# Check if the selected movie is already in our preloaded data.
if movie_selected and movie_selected.lower() in [movie["title"].lower() for movie in preloaded_movies]:
    st.error("This movie is already in our database. Please select a different movie.")

if st.button("Find Similar Movies") and movie_selected:
    with st.spinner("Fetching movie details and computing similarities..."):
        try:
            new_movie = fetch_movie_data(movie_selected)
            new_title = new_movie["title"]
            new_summary = new_movie["summary"]
            new_genres = new_movie["genres"]
            st.subheader(f"Results for **{new_title}**")
            st.write("**Overview:**", new_summary)
            st.write("**Genres:**", ", ".join(new_genres) if new_genres else "N/A")
            
            # Compute similarity between the query movie's summary and the preloaded movies.
            indices, scores = compute_similarity(new_summary, index, model)
            st.markdown("### Top 2 Similar Movies from Database")
            for rank, (idx, score) in enumerate(zip(indices, scores), start=1):
                rec_movie = preloaded_movies[idx]
                rec_title = rec_movie["title"]
                rec_summary = rec_movie["summary"]
                rec_genres = rec_movie["genres"]
                shared = list(set(new_genres) & set(rec_genres))
                shared_str = ", ".join(shared) if shared else "No common genres found"
                st.markdown(f"**{rank}. {rec_title}**")
                st.write(f"Similarity Score: **{round(score * 100, 2)}%**")
                st.write(f"Shared Genres: {shared_str}")
                st.write(f"**Summary:** {rec_summary}")
                st.markdown("---")
        except Exception as e:
            st.error(str(e))
