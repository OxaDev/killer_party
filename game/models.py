from django.db import models

class Game(models.Model):
    code = models.CharField(max_length=6, unique=True)
    players = models.JSONField(default=list)  # List of player names
    targets = models.JSONField(default=dict)  # Mapping of player to target
    methods = models.JSONField(default=dict)  # Mapping of player to method

class Player(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)