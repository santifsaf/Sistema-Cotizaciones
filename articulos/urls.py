from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_articulos, name="mis_articulos"),
    path('nuevo/', views.nuevo_articulo, name="nuevo_articulo"),
    path('eliminar_articulo/', views.eliminar_articulo, name='eliminar_articulo'),
    path('actualizar_articulo/<int:articulo_id>/', views.actualizar_articulo, name='actualizar_articulo'),
]