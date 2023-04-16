from django.db import models
from django.contrib.auth.models import User

class mymovdb_movieinfo(models.Model):
    moviename = models.CharField(max_length=300, unique=True)
    releaseyear = models.CharField(max_length=4, default='')
    rating = models.FloatField(default=0)
    description = models.TextField(default='')
    poster = models.CharField(max_length=500, default='')
    genres = models.CharField(max_length=500, default='')
    runtime = models.IntegerField(default=0)
    budget = models.BigIntegerField(null=True)
    revenue = models.BigIntegerField(null=True)
    production_companies = models.CharField(max_length=1000, default='')
    tagline = models.CharField(max_length=1000, default='')
    backdrop_path = models.CharField(max_length=1000, default='')
    vote_average = models.FloatField(null=True)
    director = models.CharField(max_length=300, default='')
    actors = models.CharField(max_length=1000, default='') 
    writers = models.CharField(max_length=1000, default='') 
    producers = models.CharField(max_length=1000, default='') 
    int_id = models.PositiveIntegerField(null=True, unique=True)
    pull_id = models.PositiveIntegerField(null=True, unique=True)

    def __str__(self):
        return self.moviename

    class Meta:
        db_table = 'mymovdb_movieinfo'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(mymovdb_movieinfo, related_name='favorited_by', blank=True)

    def __str__(self):
        return self.user.username
    
class Favorite(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(mymovdb_movieinfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.movie.moviename}"