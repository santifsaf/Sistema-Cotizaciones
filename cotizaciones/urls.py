from django.urls import path
from .views import MisCotizaciones, NuevaCotizacion, EliminarCotizacion, GuardarCotizacion, VerCotizacionView


urlpatterns = [
    path('', MisCotizaciones.as_view(), name="mis_cotizaciones"),
    path('nueva/', NuevaCotizacion.as_view(), name="nueva_cotizacion"),
    path('eliminar_cotizacion/', EliminarCotizacion.as_view(), name='eliminar_cotizacion'),
    path('cotizacion/nueva/', GuardarCotizacion.as_view(), name='crear_cotizacion'),
    path('cotizacion/<int:cotizacion_id>/ver/', VerCotizacionView.as_view(), name='ver_cotizacion'),
]