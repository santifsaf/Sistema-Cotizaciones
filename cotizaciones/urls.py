from django.urls import path, include
from .views import MisCotizaciones, NuevaCotizacion, EliminarCotizacion
from . import views

urlpatterns = [
    path('', MisCotizaciones.as_view(), name="mis_cotizaciones"),
    path('nueva/', NuevaCotizacion.as_view(), name="nueva_cotizacion"),
    path('eliminar_cotizacion/', EliminarCotizacion.as_view(), name='eliminar_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/pdf/', views.generar_pdf, name='generar_pdf'),
    ]