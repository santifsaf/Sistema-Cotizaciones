from django.contrib import admin
from .models import Articulos

# Register your models here.

class ArticulosAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')


admin.site.register(Articulos, ArticulosAdmin)