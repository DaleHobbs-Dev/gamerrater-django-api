"""Model for Player"""

from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    """Represents a player in the system"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return a string representation of the player"""
        # Represent a player by their first_name, last_name, and username
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"
