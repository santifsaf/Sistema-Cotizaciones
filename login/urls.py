from django.urls import path
from . import views

urlpatterns = [
    path('', views.vistaRegistro.as_view(), name="registro"),
]