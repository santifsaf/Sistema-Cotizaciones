from django.contrib import admin
from .models import Clientes
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class clientesResource(resources.ModelResource):
    class Meta:
        model = Clientes


class ClientesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields=('created', 'updated')
    resource_class=clientesResource

admin.site.register(Clientes, ClientesAdmin)