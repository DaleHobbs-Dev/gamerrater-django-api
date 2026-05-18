"""Report View Functions for the Gamer Rater API"""

from django.shortcuts import render
from raterapi.models import GameRating


def ratings_report(request):
    """View function to generate a report of game ratings."""

    # Query the GameRating model to get all ratings, including related game and player information
    # Using select_related to optimize database queries by fetching related objects in a single query
    ratings = GameRating.objects.select_related("game", "player").all()

    # Prepare the context for the template
    context = {"ratings": ratings}

    # Render the 'ratings.html' template with the context data
    return render(request, "reports/ratings.html", context)
