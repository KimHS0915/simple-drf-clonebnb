from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    path("", views.rooms_view),
    path("search/", views.search_room),
    path("<int:pk>/", views.room_view),
]
