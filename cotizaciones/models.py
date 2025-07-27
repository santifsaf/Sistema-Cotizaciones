from django.db import models
from cotizApp.models import Empresa
from clientes.models import Clientes
from articulos.models import Articulo
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
from django.db.models import Max, IntegerField
from django.db import transaction
from django.db.models.functions import Substr, Cast

class Cotizaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    condiciones_pago = models.CharField(max_length=50, null=True, blank=True)
    numero_referencia=models.CharField(unique=True, editable=False, blank=True, max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    cliente=models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_con_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    def calcular_totales(self):
        """
        Calcula el total, el descuento aplicado y el total con descuento de la cotización.
        """
        articulos = self.items.all()
        total = Decimal('0.00')

        try:
            descuento = Decimal(str(self.descuento).replace(",", ".")) if self.descuento else Decimal('0.00')
        except InvalidOperation:
            descuento = Decimal('0.00')

        # Validación de rango de descuento
        descuento = max(Decimal('0.00'), min(descuento, Decimal('100.00')))

        for item in articulos:
            precio_unitario = item.articulo.precio or Decimal('0.00')
            if self.condiciones_pago == 'Efectivo':
                precio_unitario *= (Decimal('1.00') - (descuento / 100))
            subtotal = precio_unitario * item.cantidad
            total += subtotal

        descuento_monto = total * (descuento / 100)
        total_con_descuento = total - descuento_monto

        if total_con_descuento < 0:
            total_con_descuento = Decimal('0.00')

        return total, descuento, total_con_descuento

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar automáticamente el número de referencia.
        """
        if not self.numero_referencia:
            with transaction.atomic():
                ultimo_num = (
                    Cotizaciones.objects
                    .annotate(numero=Cast(Substr('numero_referencia', 5), IntegerField()))
                    .aggregate(ultimo=Max('numero'))['ultimo'] or 0
                )
                nuevo_num = ultimo_num + 1
                self.numero_referencia = f'COT-{nuevo_num:05d}'
        super().save(*args, **kwargs)


class ArticulosCotizado(models.Model):
    """
    Modelo que representa un artículo cotizado dentro de una cotización.
    """
    cotizacion = models.ForeignKey(Cotizaciones, on_delete=models.CASCADE, related_name='items')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        """
        Calcula el subtotal del artículo cotizado, considerando descuento por pago en efectivo.
        """
        precio_unitario = self.articulo.precio or Decimal('0.00')
        if self.cotizacion.condiciones_pago == 'Efectivo':
            precio_unitario *= Decimal('0.90')  # 10% off
        return precio_unitario * self.cantidad