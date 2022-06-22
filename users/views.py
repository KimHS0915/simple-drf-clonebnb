from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def me_view(request):

    if (request.method == "GET"):
        serializer = ReadUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif (request.method == "PUT"):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = ReadUserSerializer(user)
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_view(request, pk):
    if (request.method == "GET"):
        try:
            user = User.objects.get(pk=pk)
            serializer = ReadUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


