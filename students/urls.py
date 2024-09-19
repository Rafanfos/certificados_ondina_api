from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_students, name='register_students'),
]