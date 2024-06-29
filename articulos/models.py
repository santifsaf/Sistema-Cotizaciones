from django.db import models

# Create your models here.

class Articulo(models.Model):
    imagen=models.ImageField(upload_to='articulos', default='proyectoWeb/media/articulos/sin imagen.jpg')
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
    
    