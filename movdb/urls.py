from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('mymoviedatabase/', views.mymoviedatabase, name='mymoviedatabase'),
    path('mymoviedatabase/searchresults/', views.search_results, name='search_results'),
    path('movieinfo/<int:int_id>/', views.movieinfo, name='movieinfo'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_favorite/<int:int_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:int_id>/', views.remove_favorite, name='remove_favorite'),
    path('password-reset/', views.custom_password_reset, name='custom_password_reset'),
]
