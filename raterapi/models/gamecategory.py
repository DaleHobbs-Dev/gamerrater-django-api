"""Model for GameCategory"""

from django.db import models
from .game import Game
from .category import Category


class GameCategory(models.Model):
    """Represents a category for a game"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game} - {self.category}"

    class Meta:
        unique_together = ("game", "category")
