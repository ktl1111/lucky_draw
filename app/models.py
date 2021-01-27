from django.db import models

# Create your models here.

class Result(models.Model):
    winner = models.TextField()
    prize = models.TextField()