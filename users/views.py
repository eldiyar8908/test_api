from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import  UserCreateValidateSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)  # **serializer.validated_data
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'errors': 'Username or Password wrong!'})


# @api_view(['POST'])
# def authorization_api_view(request):
#     serializer = UserLoginValidateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password) #**serializer.validated_data
#     if user:
#         token, created = Token.objects.get_or_create(user=user)
#         return Response(data={'key': token.key})
#     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'errors': 'Username or Password wrong!'})


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    return Response(status=status.HTTP_201_CREATED, data={'user_id': user.id})

