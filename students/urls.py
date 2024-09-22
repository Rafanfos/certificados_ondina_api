from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_students, name='register_students'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('list/', views.get_all_students, name='get_all_students'),
]