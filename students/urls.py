from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_students, name='register_students'),
    path('highlight-pdf', views.highlight_pdf, name='highlight_pdf'),
    path('', views.get_all_students, name='get_all_students'),
]