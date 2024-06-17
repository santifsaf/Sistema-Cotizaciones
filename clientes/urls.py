from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_clientes, name="mis clientes"),
    path('nuevo/', views.nuevo_cliente, name="nuevo cliente"),
]
