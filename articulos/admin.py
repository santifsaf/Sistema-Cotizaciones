from django.contrib import admin
from .models import Articulo
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ArticuloResource(resources.ModelResource):
    class Meta:
        model = Articulo

class ArticuloAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields=('created', 'updated')
    resource_class= ArticuloResource


admin.site.register(Articulo, ArticuloAdmin)