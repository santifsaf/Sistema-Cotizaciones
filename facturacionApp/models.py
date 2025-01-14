from django.db import models


# Create your models here.

class Empresa(models.Model):
    nombre=models.CharField(max_length=30)
    cuit=models.CharField(max_length=20)
    telefono=models.CharField(max_length=20)
    mail=models.EmailField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)

    class Meta:
        verbose_name="Empresa"
        verbose_name_plural="Empresas"

    def __str__(self):
        return self.nombre