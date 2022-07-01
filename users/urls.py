from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = "users"
router = DefaultRouter()
router.register("", views.UsersViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path("", views.create_account),
#     path("token/", views.login),
#     path("me/", views.me_view),
#     path("me/favs/", views.toggle_fav),
#     path("<int:pk>/", views.user_view),
# ]
