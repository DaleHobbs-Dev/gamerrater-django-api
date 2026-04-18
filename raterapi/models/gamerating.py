"""Model for GameRating"""

from django.db import models
from django.contrib.auth.models import User
from .game import Game


class GameRating(models.Model):
    """Represents a rating for a game"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("game", "player")

    def __str__(self):
        return f"Rating of {self.rating} for {self.game} by {self.player}"
