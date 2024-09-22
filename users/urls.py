from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from uuid import UUID
urlpatterns = [
    path("register", views.UserView.as_view()),
    path("<uuid:pk>", views.UserDetailView.as_view()),
    path("login", jwt_views.TokenObtainPairView.as_view()),
]
