from django.urls import path
from . import views
from .views import MisClientes, NuevoCliente, ActualizarCliente, EliminarCliente

urlpatterns = [
    path('', MisClientes.as_view(), name="mis_clientes"),
    path('nuevo/', NuevoCliente.as_view(), name="nuevo_cliente"),
    path('eliminar_cliente/', EliminarCliente.as_view(), name='eliminar_cliente'),
    path('actualizar_cliente/<int:pk>/', ActualizarCliente.as_view(), name='actualizar_cliente'),
]

