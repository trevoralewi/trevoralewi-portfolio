from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage),
    path('projects/', views.projects, name='projects'),
    path('resume/', views.resume, name='resume'),
    path('projects/urltoolbox/', views.urltoolbox, name='urltoolbox'),
    path('projects/mymoviedatabase/developer/', views.mymoviedatabase_developer, name='mymoviedatabase_developer'),
    path('projects/portfolio/developer/', views.portfolio_developer, name='portfolio_developer'),


]


