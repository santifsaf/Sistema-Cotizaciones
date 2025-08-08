from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from cotizApp.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('cotizApp.urls')),
    path('articulos/', include('articulos.urls')),
    path('clientes/', include('clientes.urls')),
    path('cotizaciones/', include('cotizaciones.urls')),
    path('', Home.as_view(), name='home'),
    path('login/', include('login.urls')), 
    path('accounts/', include('allauth.urls')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)