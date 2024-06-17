from django.urls import path
from . import views

urlpatterns = [
    path('', views.mis_cotizaciones, name="mis_cotizaciones"),
    path('nueva/', views.nueva_cotizacion, name="nueva_cotizacion"),
]
