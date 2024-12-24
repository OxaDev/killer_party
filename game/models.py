from django.db import models

class Game(models.Model):
    code = models.CharField(max_length=6, unique=True)
    master_code = models.CharField(max_length=20, unique=True)
    players = models.JSONField(default=list)  # List of player names
    players_codes = models.JSONField(default=dict) # List of player codes
    targets = models.JSONField(default=dict)  # Mapping of player to target
    methods = models.JSONField(default=dict)  # Mapping of player to method