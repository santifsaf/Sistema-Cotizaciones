from django.db import models
from clientes.models import Clientes
from articulos.models import Articulo
from django.contrib.auth.models import User

# Create your models here.

class Cotizaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    condiciones_pago = models.CharField(max_length=50, null=True, blank=True)
    numero_referencia=models.CharField(unique=True, editable=False, blank=True, max_length=20)
    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE)
    articulos_cotizados=models.ManyToManyField(Articulo)
    observaciones = models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.numero_referencia:
            last_cotizacion = Cotizaciones.objects.all().order_by('id').last()
            if last_cotizacion:
                last_id = last_cotizacion.id
            else:
                last_id = 0
            self.numero_referencia = f'COT-{last_id + 1:05d}'
        super().save(*args, **kwargs)

 
    class Meta:
        verbose_name="Cotizacion"
        verbose_name_plural="Cotizaciones"
    
    def __str__(self):
     return self.numero_referencia