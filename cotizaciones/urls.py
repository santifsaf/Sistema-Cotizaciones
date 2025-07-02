from django.urls import path
from .views import MisCotizaciones, NuevaCotizacion, EliminarCotizacion, GuardarCotizacion, generar_pdf
from . import views

urlpatterns = [
    path('', MisCotizaciones.as_view(), name="mis_cotizaciones"),
    path('nueva/', NuevaCotizacion.as_view(), name="nueva_cotizacion"),
    path('eliminar_cotizacion/', EliminarCotizacion.as_view(), name='eliminar_cotizacion'),
    path('cotizacion/nueva/', GuardarCotizacion.as_view(), name='crear_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/pdf/', views.generar_pdf, name='generar_pdf'),
    ]