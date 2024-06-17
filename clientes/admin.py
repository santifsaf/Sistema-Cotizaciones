from django.contrib import admin
from .models import Clientes

# Register your models here.

class ClientesAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

admin.site.register(Clientes, ClientesAdmin)