from django.urls import path
from .views import MisCotizaciones, NuevaCotizacion, EliminarCotizacion


urlpatterns = [
    path('', MisCotizaciones.as_view(), name="mis_cotizaciones"),
    path('nueva/', NuevaCotizacion.as_view(), name="nueva_cotizacion"),
    path('eliminar_cotizacion/', EliminarCotizacion.as_view(), name='eliminar_cotizacion'),
]
