from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Clientes(models.Model):
    usuario_log=models.ForeignKey(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=50)
    nombre_empresa=models.CharField(null=True, max_length=30)
    cuit=models.CharField(max_length=20)
    telefono=models.CharField(max_length=20)
    mail=models.EmailField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

    def __str__(self):
        return f"{self.nombre_empresa} - {self.nombre}"