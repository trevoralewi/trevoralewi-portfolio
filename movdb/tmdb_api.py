import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mymoviedb.settings")
import django
django.setup()
import requests
from django.db import IntegrityError
from django.conf import settings
from movdb.models import mymovdb_movieinfo
print(f"Using database: {settings.DATABASES['default']['NAME']}")

def get_all_movie_data():
    url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits'
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

    for movie_id in movie_ids:
        response = requests.get(url.format(movie_id=movie_id, api_key=api_key))
        data = response.json()

        # Extract other movie details
        moviename = data.get('title')
        releaseyear = data.get('release_date', '')[:4]
        rating = data.get('vote_average', 0)
        description = data.get('overview', '')
        poster = data.get('poster_path', '')
        genres = ", ".join([genre["name"] for genre in data.get("genres", [])])
        runtime = data.get("runtime", 0)
        budget = data.get('budget', None)
        revenue = data.get('revenue', None)
        production_companies = ", ".join([company["name"] for company in data.get("production_companies", [])])
        tagline = data.get('tagline', '')
        backdrop_path = data.get('backdrop_path', '')
        vote_average = data.get('vote_average', None)
        int_id = data.get('id', None)
        pull_id = data.get('id', None)


        credits = data.get('credits', {})
        crew = credits.get('crew', [])

        director = None
        writers = []
        producers = []

        for member in crew:
            job = member.get('job')
            if job == 'Director':
                director = member.get('name')
            elif job in ['Writer', 'Screenplay', 'Author', 'Scenario Writer']:
                writers.append(member.get('name'))
            elif job == 'Producer':
                producers.append(member.get('name'))

        writers_str = ", ".join(writers)
        producers_str = ", ".join(producers)

        actors = ", ".join([actor["name"] for actor in credits.get('cast', [])[:5]])

        try:
            movie, created = mymovdb_movieinfo.objects.update_or_create(
                moviename=moviename,
                defaults={
                    'releaseyear': releaseyear,
                    'rating': rating,
                    'description': description,
                    'poster': poster,
                    'genres': genres,
                    'runtime': runtime,
                    'budget': budget,
                    'revenue': revenue,
                    'production_companies': production_companies,
                    'tagline': tagline,
                    'backdrop_path': backdrop_path,
                    'vote_average': vote_average,
                    'director': director,
                    'actors': actors,
                    'writers': writers_str,
                    'producers': producers_str,
                    'pull_id': pull_id,
                    'int_id': int_id,
                  
                }
            )
            movie.save()
        except IntegrityError:
            print(f"IntegrityError occurred while processing movie with id: {movie_id}")
        except Exception as e:
            print(f"An error occurred while processing movie with id: {movie_id}")
            print(f"Error: {e}")

if __name__ == "__main__":
    get_all_movie_data()
    movies = mymovdb_movieinfo.objects.all()
    print("Printing all movies in the database:")
    for movie in movies:
        print(movie)