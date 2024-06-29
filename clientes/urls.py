from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_clientes, name="mis_clientes"),
    path('nuevo/', views.nuevo_cliente, name="nuevo_cliente"),
    path('eliminar_cliente/', views.eliminar_cliente, name='eliminar_cliente'),
    path('actualizar_cliente/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
]
