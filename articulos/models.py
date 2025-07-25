from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Articulo(models.Model):
    usuario_log=models.ForeignKey(User, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to='articulos', default='proyectoWeb/media/articulos/sin imagen.jpg', blank=True, null=True)
    nombre=models.CharField(max_length=30)
    descripcion=models.CharField(max_length=80)
    precio=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    
    class Meta:
        verbose_name="Articulo"
        verbose_name_plural="Articulos"

    def __str__(self):
        return self.nombre
    
    