from django.shortcuts import render
import requests
from .models import *


def homepage(request):
    return render(request, 'homepage.html')

def projects(request):
    return render(request, 'projects.html')

def resume(request):
    return render(request, 'resume.html')

def urltoolbox(request):
    return render(request, 'url_toolbox.html')

def mymoviedatabase_developer(request):
    return render(request, 'mymoviedb_developer.html')

def portfolio_developer(request):
    return render(request, 'portfolio_developer.html')

