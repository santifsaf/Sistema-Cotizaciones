from django.contrib import admin
from .models import Articulo

# Register your models here.

class ArticuloAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')


admin.site.register(Articulo, ArticuloAdmin)