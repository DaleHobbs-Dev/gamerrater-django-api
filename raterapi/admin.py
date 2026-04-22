"""Admin for raterapi models"""

from django.contrib import admin
from raterapi.models import (
    Game,
    Category,
    GamePicture,
    GameRating,
    Player,
    GameCategory,
)

admin.site.register(Game)
admin.site.register(Category)
admin.site.register(GamePicture)
admin.site.register(GameRating)
admin.site.register(GameCategory)
admin.site.register(Player)
