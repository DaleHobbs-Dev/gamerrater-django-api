"""Model for Game"""

from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    """Represents a game in the system"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    designer = models.CharField(max_length=100)
    year_released = models.IntegerField(blank=True, null=True)
    num_players = models.IntegerField(blank=True, null=True)
    time_to_play = models.IntegerField(blank=True, null=True)
    age_recommendation = models.IntegerField(blank=True, null=True)
    categories = models.ManyToManyField(
        "Category", through="GameCategory", related_name="games"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the game"""
        # Return the title of the game followed by the designer
        # This is useful in Django admin and other places where a string
        # representation of the object is needed

        return f"{self.title} by {self.designer}"

    class Meta:
        unique_together = ("title", "user")
