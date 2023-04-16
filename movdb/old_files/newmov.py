import os
import requests
from datetime import datetime
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviedb.settings")
import django
django.setup()
from django.db import IntegrityError
from movdb.models import NewMovie

API_KEY = '004247aa62d2a2affb19960dc813aee1'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/original'
NOW_PLAYING_URL = 'https://api.themoviedb.org/3/movie/now_playing'

def upload_new_movies():
    response = requests.get(NOW_PLAYING_URL, params={'api_key': API_KEY, 'language': 'en-US', 'page': 1})
    now_playing = response.json().get('results', [])

    for movie_data in now_playing:
        title = movie_data.get('title')
        poster_path = POSTER_BASE_URL + movie_data.get('poster_path') if movie_data.get('poster_path') else None
        release_date_str = movie_data.get('release_date')
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date() if release_date_str else None

        # Add any other parameters you want to include here

        # Overwrite any existing entries with the same title
        existing_movies = NewMovie.objects.filter(title=title)
        if existing_movies.exists():
            existing_movies.delete()

        # Create a new newmovie object with the data
        new_movie = NewMovie(title=title, poster_path=poster_path, release_date=release_date)
        new_movie.save()

        print(f"Uploaded {title} to newmovie table.")

if __name__ == "__main__":
    upload_new_movies()
    new_movies = NewMovie.objects.all()
    print("Printing all movies in the newmovie table:")
    for movie in new_movies:
        print(movie)
