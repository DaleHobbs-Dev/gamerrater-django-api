"""URL configuration for raterproject."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from raterapi.views import UserViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path("register", UserViewSet.as_view({"post": "register_account"}), name="register"),
    path("me", UserViewSet.as_view({"get": "me"}), name="me"),
]
