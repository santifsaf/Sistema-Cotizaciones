from django.contrib import admin
from .models import Cotizaciones


class CotizacionesAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

admin.site.register(Cotizaciones, CotizacionesAdmin) 