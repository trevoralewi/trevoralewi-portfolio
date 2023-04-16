from django.shortcuts import render
from django.http import HttpResponse
import random
import requests
from django.db.models import Q, Case, When, Value, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UsernamePasswordResetForm
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect



def mymoviedatabase(request):
    poster_urls, int_ids = newmovie(request)
    context = {
        'poster_url1': poster_urls[0],
        'poster_url2': poster_urls[1],
        'poster_url3': poster_urls[2],
        'poster_url4': poster_urls[3],
        'poster_url5': poster_urls[4],
        'poster_url6': poster_urls[5],
        'poster_url7': poster_urls[6],
        'poster_url8': poster_urls[7],
        'poster_url9': poster_urls[8],
        'int_id1': int_ids[0],
        'int_id2': int_ids[1],
        'int_id3': int_ids[2],
        'int_id4': int_ids[3],
        'int_id5': int_ids[4],
        'int_id6': int_ids[5],
        'int_id7': int_ids[6],
        'int_id8': int_ids[7],
        'int_id9': int_ids[8],
    }
    return render(request, 'mymoviedb.html', context)

def newmovie(request):
    api_key = '004247aa62d2a2affb19960dc813aee1'
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}'
    response = requests.get(url)
    movie_results = response.json()['results']
    
    # Check if the movie exists in the database
    filtered_movie_results = [movie for movie in movie_results if mymovdb_movieinfo.objects.filter(int_id=movie['id']).exists()]
    random_movies = random.sample(filtered_movie_results, min(len(filtered_movie_results), 18))


    poster_urls = [f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}' for movie in random_movies]
    int_ids = [movie['id'] for movie in random_movies] 

    return poster_urls, int_ids  


def search_results(request):
    query = request.GET.get('query', '')
    results = mymovdb_movieinfo.objects.filter(Q(moviename__icontains=query) | Q(description__icontains=query)).annotate(
        custom_order=Case(
            When(moviename__icontains=query, then=Value(1)),
            When(description__icontains=query, then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    ).order_by('custom_order', '-revenue')  

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 20)  # Show 20 results per page

    try:
        paginated_results = paginator.page(page)
    except PageNotAnInteger:
        paginated_results = paginator.page(1)
    except EmptyPage:
        paginated_results = paginator.page(paginator.num_pages)

    # Check favorites for each result
    for result in paginated_results:
        result.is_favorite = False
        if request.user.is_authenticated and request.user.userprofile.favorites.filter(int_id=result.int_id).exists():
            result.is_favorite = True

    context = {
        'query': query,
        'results': paginated_results,
    }
    return render(request, 'searchresults.html', context)

def movieinfo(request, int_id):
    movie = get_object_or_404(mymovdb_movieinfo, int_id=int_id)
    movie.is_favorite = False
    if request.user.is_authenticated and request.user.userprofile.favorites.filter(int_id=movie.int_id).exists():
        movie.is_favorite = True
    context = {'movie': movie}
    return render(request, 'movieinfo.html', context)

def user_login(request):
    error_message = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mymoviedatabase')
        else:
            error_message = "Invalid username or password."
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('mymoviedatabase')



@login_required
def add_favorite(request, int_id):
    movie = get_object_or_404(mymovdb_movieinfo, int_id=int_id)
    user_profile = request.user.userprofile
    user_profile.favorites.add(movie)

    next_url = request.GET.get('next', 'mymoviedatabase')
    return redirect(next_url)


def remove_favorite(request, int_id):
    if request.method == "POST":
        movie = get_object_or_404(mymovdb_movieinfo, int_id=int_id)
        user_profile = request.user.userprofile
        user_profile.favorites.remove(movie)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})
    
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration Successful')
            return redirect('mymoviedatabase')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}

    if messages.get_level(request) == messages.SUCCESS:
        context['registration_success'] = True

    return render(request, 'register.html', context)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print(f"New user registered: {instance.username}. UserProfile created for this user.")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


def custom_password_reset(request):
    if request.method == 'POST':
        form = UsernamePasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            new_password = form.cleaned_data.get('password1')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Username not found'})

            if user.check_password(new_password):
                return JsonResponse({'success': False, 'error': 'New password is the same as the current password'})

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'})
    else:
        form = UsernamePasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

