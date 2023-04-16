import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviedb.settings")
import django
django.setup()
import requests
from django.db import IntegrityError
from django.conf import settings
from movdb.models import Movieinfo
print(f"Using database: {settings.DATABASES['default']['NAME']}")

def get_all_movie_data():
    # Use the TMDB API to get a list of all movie IDs
    url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    api_key = '004247aa62d2a2affb19960dc813aee1'
    page = 1
    movie_ids = []
    while True:
        response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}')
        data = response.json()
        if 'results' in data and data['results']:
            movie_ids.extend([result['id'] for result in data['results']])
            page += 1
        else:
            break

    # Use the list of movie IDs to get the associated information for each movie
    for movie_id in movie_ids:
        # Check if the movie already exists in the database
        movie_exists = Movieinfo.objects.filter(movie_id=movie_id).exists()
        if movie_exists:
            continue

        response = requests.get(url.format(movie_id=movie_id, api_key=api_key))
        data = response.json()

        # Extract the relevant data from the response
        movie_id = movie_id
        moviename = data.get('title')
        releaseyear = data.get('release_date', '')[:4]
        rating = data.get('vote_average', 0)
        description = data.get('overview', '')
        poster = data.get('poster_path', '')
        genres = ", ".join([genre["name"] for genre in data.get("genres", [])])
        runtime = data.get("runtime", 0)

        # Create or update a Movieinfo object with the data
        try:
            movie, created = Movieinfo.objects.update_or_create(
                movie_id=movie_id,
                defaults={
                    'moviename': moviename,
                    'releaseyear': releaseyear,
                    'rating': rating,
                    'description': description,
                    'poster': poster,
                    'genres': genres,
                    'runtime': runtime
                }
            )
            movie.save()
        except IntegrityError:
            print(f"IntegrityError occurred while processing movie with id: {movie_id}")
        except Exception as e:
            print(f"An error occurred while processing movie with id: {movie_id}")
            print(f"Error: {e}")
