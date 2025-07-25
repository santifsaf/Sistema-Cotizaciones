from django.contrib import admin
from .models import Empresa

# Register your models here.

class EmpresaAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')


admin.site.register(Empresa, EmpresaAdmin)  

  