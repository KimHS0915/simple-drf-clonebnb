from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Room
from .serializers import RoomSerializer


class RoomListView(ListAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(RetrieveAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
