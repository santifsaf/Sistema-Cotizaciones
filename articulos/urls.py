from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_articulos, name="mis_articulos"),
    path('nuevo/', views.nuevo_articulo, name="nuevo_articulo"),
]