from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('cotizApp.urls')),
    path('articulos/', include('articulos.urls')),
    path('clientes/', include('clientes.urls')),
    path('cotizaciones/', include('cotizaciones.urls')),
    path('', include('login.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)