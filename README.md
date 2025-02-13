# Movie Recommender System

This project is a movie recommendation system built with Python and Streamlit. It leverages the TMDB API to fetch movie details and uses Sentence-BERT embeddings combined with FAISS to compute semantic similarity between movies. The app then suggests movies similar in storyline and genre to the user’s query.


## Features

**TMDB API Integration:**
The api.py module handles all interactions with the TMDB API. It searches for a movie by name, retrieves its unique ID, and then fetches detailed information (summary and genres). 

**Similarity Calculation:**
The model.py module loads the Sentence-BERT model "all-MiniLM-L6-v2" to compute embeddings of movie summaries. These embeddings are normalized and indexed with FAISS to enable quick retrieval of similar movies.

**Embedding Model Selection:**
- The Sentence-BERT model ("all-MiniLM-L6-v2") is used to convert movie summaries into high-dimensional vectors (embeddings). We use Sentence-BERT (all-MiniLM-L6-v2) because it strikes a balance between speed and accuracy for semantic similarity tasks. It’s lightweight and efficient for real-time applications like this recommender.

- Each embedding is normalized so that the cosine similarity (computed as the inner product of normalized vectors) accurately reflects semantic similarity.

## FAISS Index

  FAISS was selected because it can handle large datasets efficiently and supports fast approximate nearest neighbor searches, which makes FAISS ideal for real-time recommendation systems where speed and accuracy are crucial.

- **What is FAISS?**  
  FAISS (Facebook AI Similarity Search) is a library developed for efficient similarity search in high-dimensional spaces.

- **How It Works:**  
  - The normalized embeddings are added to a FAISS index created with an inner-product metric.
  - When a new query (movie summary) is provided, its embedding is computed and normalized.
  - The FAISS index is then searched to retrieve the top similar movies based on **cosine similarity**.

## Project Structure

movie-recommender/ 
├── preloaded_movies.json # JSON file containing preloaded movie data 
├── data.py # Loads and processes JSON movie data 
├── api.py # Handles TMDB API integration for movie details 
├── model.py # Loads Sentence-BERT model, computes embeddings, sets up FAISS index, and calculates similarity 
├── ui.py # Main Streamlit application (frontend) 
├── assets/ 
│ └── style.css # External CSS for styling marquees and other UI elements 
├── config.py # Handling yaml config file(s) 
├── config.yml # For constants like paths
├── requirements.txt # List of Python dependencies 
└── README.md # This file

## Setup Instructions

1. **Clone the Repository:**

   `git clone git@github.com:cation03/movie-recommender.git
   cd movie-recommender`
   
**2. Install Dependencies:**

  Make sure you have Python 3.7 or newer installed, then run:
  `pip install -r requirements.txt`

**3. Configure Environment Variables:**

  `TMDB_API_KEY=your_tmdb_api_key_here`

**4. Launch the Streamlit app:**   

   `streamlit run ui.py`
