"""Views for handling GamePicture Related API endpoints"""

import uuid
import base64
from django.core.files.base import ContentFile
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from raterapi.models import GamePicture


class GamePictureSerializer(serializers.ModelSerializer):
    """Serializer for the GamePicture model."""

    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    class Meta:
        model = GamePicture
        fields = [
            "id",
            "game",
            "action_pic",
            "is_owner",
        ]


class GamePictureViewSet(viewsets.ViewSet):
    """ViewSet for handling GamePicture CRUD operations."""

    def list(self, request):
        """Handle GET requests to list all game pictures."""
        game_id = request.query_params.get("game_id", None)

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
        """Handle POST requests to upload a game picture.

        Expects request.data to include:
          - game: the game id
          - action_pic: a base64-encoded image string (e.g. "data:image/jpeg;base64,...")
        """

        # Split the base64 string to get the image format and the actual base64 data
        img_format, imgstr = request.data["action_pic"].split(";base64,")

        # Extract the file extension from the image format (e.g. "data:image/jpeg" -> "jpeg")
        ext = img_format.split("/")[-1]

        # Decode the base64 string and create a ContentFile object with a unique filename
        image_data = ContentFile(
            base64.b64decode(imgstr),
            name=f'{request.data["game"]}-{uuid.uuid4()}.{ext}',
        )

        # Create the GamePicture instance and save the image
        game_picture = GamePicture.objects.create(
            game_id=request.data["game"],
            user=request.user,
        )
        game_picture.action_pic.save(image_data.name, image_data, save=True)

        serializer = GamePictureSerializer(game_picture, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game picture by its primary key (pk)."""
        try:
            game_picture = GamePicture.objects.get(pk=pk)
            game_picture.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GamePicture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
