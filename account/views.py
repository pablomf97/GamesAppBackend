from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User as DjangoUser

from .models import Account
from .serializers import RegistrationSerializer


class RegisterUserView(APIView):
    permission_classes = [~IsAuthenticated]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Successfully registered new user."
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors

        return Response(data)


class DeleteTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"},
                        status=status.HTTP_200_OK)
