import requests
from config import Config


def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={Config.TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    return response.json()


def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={Config.TMDB_API_KEY}"
    response = requests.get(url)
    return response.json()
