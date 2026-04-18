"""Model for Category"""

from django.db import models


class Category(models.Model):
    """Represents a category for games"""

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        """Return a string representation of the category"""
        # Represent a category by its name
        return str(self.name)

    class Meta:
        """Ensure that each category name is unique"""

        unique_together = ("name",)
