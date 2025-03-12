from django.db import models

class Sport(models.Model):
  name = models.CharField(max_length=30, unique=True)

class Competition(models.Model):
  name = models.CharField(max_length=30, unique=True)
  sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

class Match(models.Model):
  home = models.CharField(max_length=30)
  away = models.CharField(max_length=30)
  match_date = models.DateTimeField()
  championship = models.ForeignKey(Competition, on_delete=models.CASCADE)

class Prediction(models.Model):
  match = models.OneToOneField(Match, on_delete=models.CASCADE)
  resultat = models.CharField(max_length=90)