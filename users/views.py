from django.conf import settings
from django.contrib.auth import authenticate
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rooms.models import Room
from rooms.serializers import RoomSerializer
from .serializers import UserSerializer
from .models import User


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def me_view(request):

    if request.method == "GET":
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_view(request, pk):
    if request.method == "GET":
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def toggle_fav(request):

    if request.method == "GET":
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response(status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_account(request):

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user)
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):

    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        encoded_jwt = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
        return Response(data={"token": encoded_jwt})