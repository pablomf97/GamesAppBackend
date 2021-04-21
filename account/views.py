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
from .pagination import ResultSetPagination


class RegisterUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
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


# Messing with account games
class AddGameToAccount(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, game_id):
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


class GetAccountGames(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = GameSerializer
    pagination_class = ResultSetPagination

    def get_queryset(self):
        user = self.request.user

        return user.games.all().order_by('id')


class DeleteTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"},
                        status=status.HTTP_200_OK)
