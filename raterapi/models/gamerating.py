"""Model for GameRating"""

from django.db import models
from django.contrib.auth.models import User
from .game import Game


class GameRating(models.Model):
    """Represents a rating for a game"""

    # The related_name "ratings" allows us to access all ratings for a game using game.ratings
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ratings")
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("game", "player")

    def __str__(self):
        return f"Rating of {self.rating} for {self.game} by {self.player}"
