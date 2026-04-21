"""URL configuration for raterproject."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from raterapi.views import (
    UserViewSet,
    CategoryViewSet,
    GamePictureViewSet,
    GameRatingViewSet,
    GameViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"games", GameViewSet, basename="game")
router.register(r"gamepictures", GamePictureViewSet, basename="gamepicture")
router.register(r"gameratings", GameRatingViewSet, basename="gamerating")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
    path("me", UserViewSet.as_view({"get": "me"}), name="me"),
]
