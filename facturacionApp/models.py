from django.db import models


# Create your models here.

class Cotizaciones(models.Model):
    numero_referencia=models.IntegerField(unique=True, editable=False)
    cliente=models.CharField(max_length=50)
    total_cotizado=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs): 
        if not self.id:
            self.referencia = f'COT-{self.id}'
        super().save(*args, **kwargs)
 
    class Meta:
        verbose_name="Cotizacion"
        verbose_name_plural="Cotizaciones"
    
    def __str__(self):
     return self.numero_referencia


class Clientes(models.Model):
    nombre=models.CharField(max_length=50)
    nombre_empresa=models.CharField(null=True, max_length=30)
    telefono=models.CharField(max_length=20)
    mail=models.EmailField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

    def __str__(self):
        return f"{self.nombre_empresa} - {self.nombre}"
        

class Articulos(models.Model):
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

class Empresa(models.Model):
    logo=models.ImageField(upload_to='logos', null=True)
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