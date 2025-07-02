from django.db import models
from facturacionApp.models import Empresa
from clientes.models import Clientes
from articulos.models import Articulo
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import Max
from django.db import transaction
# Create your models here.

class Cotizaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    condiciones_pago = models.CharField(max_length=50, null=True, blank=True)
    numero_referencia=models.CharField(unique=True, editable=False, blank=True, max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)
    cliente=models.ForeignKey(Clientes, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_con_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    
    def calcular_totales(self):
        total_base = Decimal('0.00')
        for item in self.items.all():
            cantidad = Decimal(str(item.cantidad))
            precio = Decimal(str(item.articulo.precio))
            total_base += cantidad * precio

        descuento = Decimal(str(self.descuento)) if self.descuento else Decimal('0.00')
        costo_envio = Decimal(str(self.costo_envio)) if self.costo_envio else Decimal('0.00')

        if descuento > 0:
            monto_descuento = (total_base * descuento) / Decimal('100.00')
            total_con_descuento = total_base - monto_descuento + costo_envio
        else:
            monto_descuento = Decimal('0.00')
            total_con_descuento = total_base + costo_envio

        return (
            total_base.quantize(Decimal('0.01')),
            monto_descuento.quantize(Decimal('0.01')),
            total_con_descuento.quantize(Decimal('0.01'))
        )
    
    def save(self, *args, **kwargs):
        if not self.numero_referencia:
            with transaction.atomic():
                # Obtener el último ID de manera segura
                ultimo_id = Cotizaciones.objects.aggregate(
                    ultimo_id=Max('id')
                )['ultimo_id'] or 0
                
                # Si no hay cotizaciones, empezar desde 1
                nuevo_id = ultimo_id + 1 if ultimo_id else 1
                self.numero_referencia = f'COT-{nuevo_id:05d}'
        
        super().save(*args, **kwargs)

 
    class Meta:
        verbose_name="Cotizacion"
        verbose_name_plural="Cotizaciones"
    
    def __str__(self):
     return self.numero_referencia


class ArticulosCotizado(models.Model):
    cotizacion = models.ForeignKey(Cotizaciones, on_delete=models.CASCADE, related_name='items')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.articulo.precio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.articulo.nombre} en Cotización #{self.cotizacion.id}"