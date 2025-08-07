from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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

    def clean(self):
        """Validaciones personalizadas del modelo"""
        super().clean()
        
        if self.precio is not None and self.precio < 0:
            raise ValidationError({
                'precio': 'El precio no puede ser negativo.'
            })    
    
    def save(self, *args, **kwargs):
        """Ejecutar validaciones antes de guardar"""
        self.full_clean() 
        super().save(*args, **kwargs)