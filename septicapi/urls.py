from django.urls import path
from . import views

urlpatterns = [
    path('home/septic', views.septic, name='septic'),
]
