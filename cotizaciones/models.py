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
        Calcula totales:
        - total: subtotal sin descuento
        - total_con_descuento: total con descuento aplicado
        """
        articulos = self.items.all()
        subtotal = Decimal('0.00')

        # Validar descuento
        try:
            descuento_pct = (
                Decimal(str(self.descuento).replace(",", "."))
                if self.descuento else Decimal('0.00')
            )
        except InvalidOperation:
            descuento_pct = Decimal('0.00')

        descuento_pct = max(Decimal('0.00'), min(descuento_pct, Decimal('100.00')))

        # Calcular subtotal (sin descuento)
        for item in articulos:
            precio = item.articulo.precio or Decimal('0.00')
            subtotal += precio * item.cantidad

        # Aplicar descuento al subtotal
        descuento_monto = subtotal * (descuento_pct / 100)
        total_con_descuento = max(subtotal - descuento_monto, Decimal('0.00'))

        return subtotal, descuento_pct, total_con_descuento

    def save(self, *args, **kwargs):
        """
        1) Genera 'numero_referencia' único si no existe.
        2) Recalcula y asigna 'total' y 'total_con_descuento' antes de guardar.
        3) Llama al super().save().
        """
        if not self.numero_referencia:
            with transaction.atomic():
                ultimo = (
                    Cotizaciones.objects
                    .annotate(n=Cast(Substr('numero_referencia', 5), IntegerField()))
                    .aggregate(maxn=Max('n'))['maxn'] or 0
                )
                self.numero_referencia = f'COT-{ultimo+1:05d}'

        subtotal, _, total_con_desc = self.calcular_totales()
        self.total = subtotal
        self.total_con_descuento = total_con_desc

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