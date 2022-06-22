from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


@api_view(["GET", "POST"])
def rooms_view(request):

    if (request.method == "GET"):
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    elif (request.method == "POST"):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room)
            return Response(data=room_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def get_room(pk):
    try:
        room = Room.objects.get(pk=pk)
        return room
    except Room.DoesNotExist:
        return None


@api_view(["GET", "PUT", "DELETE"])
def room_view(request, pk):

    if (request.method == "GET"):
        room = get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReadRoomSerializer(room)
        return Response(data=serializer.data)

    elif (request.method == "PUT"):
        room = get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serialized_data = WriteRoomSerializer(room, data=request.data, partial=True)
        if serialized_data.is_valid():
            room = serialized_data.save()
            serializer = ReadRoomSerializer(room)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == "DELETE"):
        room = get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)        
        room.delete()
        return Response(status=status.HTTP_200_OK)
