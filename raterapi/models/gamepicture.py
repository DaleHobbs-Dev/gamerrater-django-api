"""Model for GamePicture"""

from django.db import models
from django.contrib.auth.models import User
from .game import Game


def game_image_upload_path(instance, filename):
    return f"actionimages/{instance.game_id}/{filename}"


class GamePicture(models.Model):
    """Represents a picture for a game"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="pictures")
    # action_pic is an ImageField that allows users to upload images, the upload_to parameter specifies the directory within MEDIA_ROOT where the images will be stored, in this case "actionimages", null=True allows the field to be optional in the database
    action_pic = models.ImageField(
        upload_to=game_image_upload_path,
        null=True,
    )
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture for {self.game.title} uploaded by {self.player.username}"
