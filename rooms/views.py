from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer


@api_view(["GET", "POST"])
def rooms_view(request):

    if (request.method == "GET"):
        paginator = PageNumberPagination()
        paginator.page_size = 20
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif (request.method == "POST"):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room)
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
        serializer = RoomSerializer(room)
        return Response(data=serializer.data)

    elif (request.method == "PUT"):
        room = get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            room = serializer.save()
            room_serializer = RoomSerializer(room)
            return Response(data=room_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == "DELETE"):
        room = get_room(pk)
        if room is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)        
        room.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def search_room(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price_lte"] = max_price
    if min_price is not None:
        filter_kwargs["price_gte"] = min_price
    if beds is not None:
        filter_kwargs["beds_gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms_gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms_gte"] = bathrooms
    if lat is not None and lng is not None:
        filter_kwargs["lat_gte"] = float(lat) - 0.005
        filter_kwargs["lat_lte"] = float(lat) + 0.005
        filter_kwargs["lng_gte"] = float(lng) - 0.005
        filter_kwargs["lng_lte"] = float(lng) + 0.005
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
