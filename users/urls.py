from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("", views.create_account),
    path("me/", views.me_view),
    path("me/favs/", views.toggle_fav),
    path("<int:pk>/", views.user_view),
]
