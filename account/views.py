from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from game.models import Game
from game.serializers import GameSerializer
from .serializers import RegistrationSerializer
from GamesAPI.pagination import ResultSetPagination


class RegisterUserView(APIView):
    """
    Manages requests to /user/register
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        POST request - Register a user
        """

        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered new user."
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors

        return Response(data)


class IsGameFavourited(APIView):
    """
    Manages requests to user/is-favourites/<game_id>
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, game_id):
        """
        GET request - Checks if specified game is in favourites
        """

        user = request.user
        isFavourited = False

        try:
            games = user.games.all()
            if len(games) > 0:
                for game in games:
                    if str(game.id).lower() == game_id.lower():
                        isFavourited = True
                        break
        except:
            return Response({"message": "Could not check if game was favourited."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"is_favourited": isFavourited})


class AddGameToAccount(APIView):
    """
    Manages requests to user/add-game/<game_id>/
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, game_id):
        """
        GET request - Adds specified game to the account
        """

        user = request.user

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response(
                {"message": "That game does not exist in our database."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            if game not in user.games.all():
                try:
                    user.games.add(game)
                    user.save()
                    return Response(
                        {"message": "Game successfully added to saved games."},
                        status=status.HTTP_200_OK
                    )

                except:
                    return Response(
                        {"message": "Game could not be added to saved games."},
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {"message": "The game is already in your list!"}
                )

        except:
            return Response(
                {"message": "Oops! Something went wrong while trying to perform the operation"}
            )


class RemoveGameFromAccount(APIView):
    """
    Manages requests to user/remove-game/
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, game_id):
        """
        GET request - Removes game from account
        """

        user = request.user
        success = False

        try:
            game = user.games.filter(id=game_id)
            if game:
                user.games.remove(game[0])
                success = True
        except Exception as e:
            return Response({"message": "There was an error while trying to remove the game."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"success": success})


class GetAccountGames(ListAPIView):
    """ 
    Manages requests to user/get-games/
    """
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = GameSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self):
        """ 
        GET request - Returns the list of user's games
        """
        return self.request.user.games.all().order_by('id')


class DeleteTokenView(APIView):
    """
    Manages the requests to user/logout/
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        GET request - Deletes the token assigned to the user
        """
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"},
                        status=status.HTTP_200_OK)
