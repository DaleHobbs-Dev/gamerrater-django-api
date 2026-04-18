"""Views for handling GameRating Related API endpoints"""

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from raterapi.models import GameRating


class GameRatingSerializer(serializers.ModelSerializer):
    """Serializer for the GameRating model."""

    is_owner = serializers.SerializerMethodField()

    # returns True if the current request user is the owner of the game rating
    def get_is_owner(self, obj):
        # Model uses 'player' as the foreign key to the user who created the rating
        return self.context["request"].user == obj.player

    class Meta:
        model = GameRating
        fields = [
            "id",
            "game_id",
            "rating",
            "review",
            "is_owner",
        ]


class GameRatingViewSet(viewsets.ViewSet):
    """ViewSet for handling GameRating CRUD operations."""

    def list(self, request):
        """Handle GET requests to list all game ratings."""

        # Get the game id from the query parameters to filter game ratings by game
        game_id = request.query_params.get("game", None)

        if game_id is not None:
            game_ratings = GameRating.objects.filter(game_id=game_id)
        else:
            game_ratings = GameRating.objects.all()

        serializer = GameRatingSerializer(
            game_ratings, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single game rating by its primary key (pk)."""
        try:
            game_rating = GameRating.objects.get(pk=pk)
            serializer = GameRatingSerializer(game_rating, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GameRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = GameRatingSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(player=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game rating by its primary key (pk)."""
        try:
            game_rating = GameRating.objects.get(pk=pk)
            game_rating.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GameRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a single game rating by its primary key (pk)."""
        try:
            game_rating = GameRating.objects.get(pk=pk)
        except GameRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GameRatingSerializer(
            game_rating, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(player=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
