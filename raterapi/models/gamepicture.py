"""Model for GamePicture"""

from django.db import models
from django.contrib.auth.models import User
from .game import Game


class GamePicture(models.Model):
    """Represents a picture for a game"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="pictures")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture for {self.game}"

    class Meta:
        unique_together = ("game", "url")
