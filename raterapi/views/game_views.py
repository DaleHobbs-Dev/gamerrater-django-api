"""Views for handling game-related API endpoints"""

from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from django.db import IntegrityError
from raterapi.models import Game
from .category_views import CategorySerializer


class GameSerializer(serializers.ModelSerializer):
    """Serializer for the Game model."""

    categories = CategorySerializer(many=True, read_only=True)

    is_owner = serializers.SerializerMethodField()

    # average_rating is a read-only field that calculates the average rating for the game
    # this helps serializer know it is computed and should not be provided by the client when creating or updating a game
    average_rating = serializers.FloatField(read_only=True)

    # returns True if the current request user is the owner of the game
    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = Game
        fields = [
            "id",
            "is_owner",
            "title",
            "description",
            "designer",
            "year_released",
            "num_players",
            "time_to_play",
            "age_recommendation",
            "categories",
            "average_rating",
        ]


class GameViewSet(viewsets.ViewSet):
    """ViewSet for handling Game CRUD operations."""

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Handle GET requests to list all games."""
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single game by its primary key (pk)."""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST requests to create a new game."""
        serializer = GameSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                game: Game = serializer.save(user=request.user)
                category_ids = request.data.get("categories", [])
                game.categories.set(category_ids)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "You have already added a game with that title."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game by its primary key (pk)."""
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests to update a single game by its primary key (pk)."""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(
                game, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save(user=request.user)
                category_ids = request.data.get("categories", [])
                game.categories.set(category_ids)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        """Handle PATCH requests to partially update a single game by its primary key (pk)."""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(
                game, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save(user=request.user)
                category_ids = request.data.get("categories", [])
                if "categories" in request.data:
                    game.categories.set(category_ids)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
