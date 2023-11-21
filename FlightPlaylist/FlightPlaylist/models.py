from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    destination = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    names = models.CharField(max_length=100)
    songs = models.JSONField()