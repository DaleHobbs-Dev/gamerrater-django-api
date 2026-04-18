"""Views for handling GamePicture Related API endpoints"""

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from raterapi.models import GamePicture


class GamePictureSerializer(serializers.ModelSerializer):
    """Serializer for the GamePicture model."""

    is_owner = serializers.SerializerMethodField()

    # returns True if the current request user is the owner of the game picture
    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = GamePicture
        fields = [
            "id",
            "game_id",
            "url",
            "is_owner",
        ]


class GamePictureViewSet(viewsets.ViewSet):
    """ViewSet for handling GamePicture CRUD operations."""

    def list(self, request):
        """Handle GET requests to list all game picture urls."""

        # Get the game id from the query parameters to filter game pictures by game
        game_id = request.query_params.get("game", None)

        if game_id is not None:
            game_pictures = GamePicture.objects.filter(game_id=game_id)
        else:
            game_pictures = GamePicture.objects.all()

        serializer = GamePictureSerializer(
            game_pictures, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single game picture by its primary key (pk)."""
        try:
            game_picture = GamePicture.objects.get(pk=pk)
            serializer = GamePictureSerializer(
                game_picture, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GamePicture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = GamePictureSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game picture by its primary key (pk)."""
        try:
            game_picture = GamePicture.objects.get(pk=pk)
            game_picture.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GamePicture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
