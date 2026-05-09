"""Tests for Game model and API endpoints."""

import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from raterapi.models import Game


class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database. Order matters if there are dependencies between the models. For example, if Game has a foreign key to User, then the users fixture must be listed before the games fixture.
    fixtures = [
        "users",
        "players",
        "categories",
        "games",
        "gamepictures",
        "gameratings",
        "gamecategories",
    ]

    def setUp(self):
        self.game = Game.objects.first()
        # Authenticate as the user who owns the game. This is necessary because the view requires authentication and also assigns request.user as the owner of the game.
        # Returns a tuple of (token_object, was_it_just_created: True/False), but we only care about the token, so we unpack it as (token, _) using a _ to show we do not care about the boolean.
        token, _ = Token.objects.get_or_create(user=self.game.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/games"

        # Define the request body. No 'user' field -- the view assigns
        # request.user automatically via serializer.save(user=request.user).
        data = {
            "title": "Clue",
            "description": "A classic mystery board game.",
            "designer": "Milton Bradley",
            "year_released": 1949,
            "num_players": 6,
            "time_to_play": 60,
            "age_recommendation": 8,
            "game_image": "https://cf.geekdo-images.com/wNcbhLJGGjakYjjm1gV_kQ__itemrep/img/zxCbji0M3Ot9yTmNWlbKNF9fgQ4=/fit-in/246x300/filters:strip_icc()/pic7563466.png",
            "bgg_id": 1294,
            "categories": [1, 2],
        }

        # Initiate request and store response
        response = self.client.post(url, data, format="json")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Below are assertions to check that the response is correct.
        # assertEqual(a,b) says "Assert that a and b are equal. If they are not, the test will fail and report the difference between a and b."

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["year_released"], 1949)
        self.assertEqual(json_response["num_players"], 6)
        self.assertEqual(json_response["time_to_play"], 60)
        self.assertEqual(json_response["age_recommendation"], 8)
        self.assertEqual(
            json_response["game_image"],
            "https://cf.geekdo-images.com/wNcbhLJGGjakYjjm1gV_kQ__itemrep/img/zxCbji0M3Ot9yTmNWlbKNF9fgQ4=/fit-in/246x300/filters:strip_icc()/pic7563466.png",
        )
        self.assertEqual(json_response["bgg_id"], 1294)

        # The API returns full category objects, not just IDs. GameSerializer uses
        # CategorySerializer (nested), so the response looks like:
        # [{"id": 1, "name": "Strategy"}, {"id": 2, "name": "Dice"}]
        # We pull out just the IDs to check that the right categories were assigned.
        returned_category_ids = [cat["id"] for cat in json_response["categories"]]
        # Assert that the correct categories were assigned to the game. The categories with IDs 1 and 2 are "Strategy" and "Dice", respectively, according to the categories fixture.
        # Asserterting against the wrong shape will fail so we ensured that the response shape is correct by pulling out the IDs in a list comprehension and then asserting against that list of IDs.
        self.assertEqual(returned_category_ids, [1, 2])
        # Check that the created_at field is not present in the response but is present in the database. The GameSerializer does not include created_at, so it should not be in the response, but the Game model does have a created_at field that is automatically set when a game is created, so it should be in the database.
        self.assertNotIn("created_at", json_response)

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.user = self.game.user
        game.title = "Monopoly"
        game.description = "A classic property trading game."
        game.designer = "Milton Bradley"
        game.year_released = 1935
        game.num_players = 4
        game.time_to_play = 120
        game.age_recommendation = 8
        game.game_image = "https://cf.geekdo-images.com/9nGoBZ0MRbi6rdH47sj2Qg__itemrep/img/8EP4ErNA709diOt6fUyJH30FtbU=/fit-in/246x300/filters:strip_icc()/pic5786795.jpg"
        game.bgg_id = 1406

        # Save the game to the database so that it gets an ID and can be retrieved by the API. The game must be saved before we can set the categories because the categories field is a many-to-many relationship that requires the game to have a primary key (ID) before it can be associated with categories.
        game.save()

        game.categories.set([1, 2])

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["designer"], "Milton Bradley")
        self.assertEqual(json_response["year_released"], 1935)
        self.assertEqual(json_response["num_players"], 4)
        self.assertEqual(json_response["time_to_play"], 120)
        self.assertEqual(json_response["age_recommendation"], 8)
        self.assertEqual(
            json_response["game_image"],
            "https://cf.geekdo-images.com/9nGoBZ0MRbi6rdH47sj2Qg__itemrep/img/8EP4ErNA709diOt6fUyJH30FtbU=/fit-in/246x300/filters:strip_icc()/pic5786795.jpg",
        )
        self.assertEqual(json_response["bgg_id"], 1406)

        returned_category_ids = [cat["id"] for cat in json_response["categories"]]
        self.assertEqual(returned_category_ids, [1, 2])

    def test_update_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.user = self.game.user
        game.title = "Sorry"
        game.description = "A classic family board game."
        game.designer = "Milton Bradley"
        game.year_released = 1934
        game.num_players = 4
        game.time_to_play = 60
        game.age_recommendation = 6
        game.game_image = "https://cf.geekdo-images.com/zV33y_kLzvOuGz1_r1DWNA__itemrep/img/zWzu8glsg3surHUT6_xxaEI1pRQ=/fit-in/246x300/filters:strip_icc()/pic8204421.jpg"
        game.bgg_id = 2407
        game.save()
        game.categories.set([1, 2])

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "title": "Sorry",
            "description": "A classic family board game.",
            "designer": "Hasbro",
            "year_released": 1934,
            "num_players": 4,
            "time_to_play": 60,
            "age_recommendation": 6,
            "game_image": "https://cf.geekdo-images.com/zV33y_kLzvOuGz1_r1DWNA__itemrep/img/zWzu8glsg3surHUT6_xxaEI1pRQ=/fit-in/246x300/filters:strip_icc()/pic8204421.jpg",
            "bgg_id": 2407,
            "categories": [1, 2],
        }

        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # GET game again to verify changes were made
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], game.id)
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["description"], "A classic family board game.")
        self.assertEqual(json_response["designer"], "Hasbro")
        self.assertEqual(json_response["year_released"], 1934)
        self.assertEqual(json_response["num_players"], 4)
        self.assertEqual(json_response["time_to_play"], 60)
        self.assertEqual(json_response["age_recommendation"], 6)
        self.assertEqual(
            json_response["game_image"],
            "https://cf.geekdo-images.com/zV33y_kLzvOuGz1_r1DWNA__itemrep/img/zWzu8glsg3surHUT6_xxaEI1pRQ=/fit-in/246x300/filters:strip_icc()/pic8204421.jpg",
        )
        self.assertEqual(json_response["bgg_id"], 2407)

        returned_category_ids = [cat["id"] for cat in json_response["categories"]]
        self.assertEqual(returned_category_ids, [1, 2])

        # Switch to a different user (jsmith, pk=2) and attempt the same PUT.
        # jsmith does not own this game, so the view should reject it with 403.
        other_user = User.objects.get(pk=2)
        other_token, _ = Token.objects.get_or_create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.user = self.game.user
        game.title = "Sorry"
        game.description = "A classic family board game."
        game.designer = "Milton Bradley"
        game.year_released = 1934
        game.num_players = 4
        game.time_to_play = 60
        game.age_recommendation = 6
        game.game_image = "https://cf.geekdo-images.com/zV33y_kLzvOuGz1_r1DWNA__itemrep/img/zWzu8glsg3surHUT6_xxaEI1pRQ=/fit-in/246x300/filters:strip_icc()/pic8204421.jpg"
        game.bgg_id = 2407
        game.save()
        game.categories.set([1, 2])

        # Switch to a different user (jsmith, pk=2) and attempt the DELETE.
        # jsmith does not own this game, so the view should reject it with 403.
        other_user = User.objects.get(pk=2)
        other_token, _ = Token.objects.get_or_create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Switch back to the owner (jdoe) and confirm they can still delete it.
        owner_token, _ = Token.objects.get_or_create(user=game.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {owner_token.key}")

        # DELETE the game you just created
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_game(self):
        """
        Ensure we can partially update an existing game (PATCH).
        Only the fields included in the request body should change.
        Fields left out of the request should remain untouched.
        """
        game = Game()
        game.user = self.game.user
        game.title = "Battleship"
        game.description = "A classic naval combat game."
        game.designer = "Milton Bradley"
        game.year_released = 1967
        game.num_players = 2
        game.time_to_play = 30
        game.age_recommendation = 7
        game.game_image = "https://cf.geekdo-images.com/E_LdMVom4a4QHGW_MJM6g__itemrep/img/DKQvEjr0_oWxSaB4KZJHK7WZiNk=/fit-in/246x300/filters:strip_icc()/pic1180873.jpg"
        game.bgg_id = 37111
        game.save()
        # Assign initial categories: Strategy (1) and Dice (2)
        game.categories.set([1, 2])

        # PATCH with only the fields we want to change. designer and num_players
        # are updated; everything else -- including categories -- is left out intentionally.
        data = {
            "designer": "Hasbro",
            "num_players": 4,
        }

        response = self.client.patch(f"/games/{game.id}", data, format="json")

        # PATCH returns 200 with the updated game in the body (same as PUT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)

        # Assert the two fields we changed were updated
        self.assertEqual(json_response["designer"], "Hasbro")
        self.assertEqual(json_response["num_players"], 4)

        # Assert the fields we did NOT send were left alone
        self.assertEqual(json_response["title"], "Battleship")
        self.assertEqual(json_response["year_released"], 1967)
        self.assertEqual(json_response["time_to_play"], 30)
        self.assertEqual(json_response["age_recommendation"], 7)

        # Categories were not included in the PATCH body. The partial_update view
        # only calls game.categories.set() when 'categories' is present in the
        # request, so these should be unchanged.
        returned_category_ids = [cat["id"] for cat in json_response["categories"]]
        self.assertEqual(returned_category_ids, [1, 2])

        # Send a second PATCH that changes only categories. This confirms that
        # multiple requests can be made within one test, and that categories are
        # only updated when explicitly included in the request body.
        data2 = {
            "categories": [2, 3],
        }

        response = self.client.patch(f"/games/{game.id}", data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = json.loads(response.content)

        # Assert categories changed to Dice (2) and Card (3)
        returned_category_ids = [cat["id"] for cat in json_response["categories"]]
        self.assertEqual(returned_category_ids, [2, 3])

        # Assert the fields from the first PATCH were not affected by the second
        self.assertEqual(json_response["designer"], "Hasbro")
        self.assertEqual(json_response["num_players"], 4)

        # Switch to a different user (jsmith, pk=2) and attempt a PATCH.
        # jsmith does not own this game, so the view should reject it with 403.
        other_user = User.objects.get(pk=2)
        other_token, _ = Token.objects.get_or_create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {other_token.key}")

        response = self.client.patch(
            f"/games/{game.id}", {"designer": "Someone Else"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
