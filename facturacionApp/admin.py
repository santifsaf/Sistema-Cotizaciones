from django.contrib import admin
from .models import Empresa, Clientes, Articulos, Cotizaciones

# Register your models here.

class EmpresaAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class ClientesAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class ArticulosAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class CotizacionesAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Clientes, ClientesAdmin)   
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(Cotizaciones, CotizacionesAdmin)   