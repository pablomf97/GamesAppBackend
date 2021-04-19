from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User as DjangoUser

from gamesapp.models import User


class RegisterUserView(APIView):
    permission_classes = [~IsAuthenticated]

    def post(self, request):
        data = request.POST
        user_name = data.get('username')
        user_password = data.get('password')

        if DjangoUser.objects.filter(username=user_name).exists():
            return Response({"message": "Sorry, username already exists"})
        else:
            new_user = DjangoUser.objects.create_user(
                username=user_name,
                password=user_password
            )
            new_user.save()

            User.objects.create(
                user=new_user
            )

            return Response({"message": "User successfully created."})


class DeleteTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
