from django.urls import path
from .views import Home
from . import views

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('mis_empresas/', views.mis_empresas, name="mis_empresas"),
    path('nueva/', views.nueva_empresa, name="nueva_empresa"),
    path('eliminar_empresa/', views.eliminar_empresa, name='eliminar_empresa'),
    path('actualizar_empresa/<int:empresa_id>/', views.actualizar_empresa, name='actualizar_empresa'),
]
