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
    numero_referencia = models.CharField(unique=True, editable=False, blank=True, max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos históricos de la empresa
    empresa_nombre = models.CharField(max_length=100, null=True, blank=True)
    empresa_cuit = models.CharField(max_length=20, null=True, blank=True)
    empresa_mail = models.EmailField(null=True, blank=True)
    empresa_telefono = models.CharField(max_length=20, null=True, blank=True)
    
    # Campos históricos del cliente
    cliente_nombre = models.CharField(max_length=100, null=True, blank=True)
    cliente_empresa = models.CharField(max_length=100, null=True, blank=True)
    cliente_cuit = models.CharField(max_length=20, null=True, blank=True)
    cliente_mail = models.EmailField(null=True, blank=True)
    
    observaciones = models.TextField(null=True, blank=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_con_descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
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
        subtotal = sum((item.articulo_precio or Decimal('0.00')) * item.cantidad for item in self.items.all())
        # Aplicar descuento al subtotal
        descuento_monto = subtotal * (descuento_pct / 100)
        total_con_descuento = max(subtotal - descuento_monto, Decimal('0.00'))

        return subtotal, descuento_pct, total_con_descuento

    def save(self, *args, **kwargs):
        """
        1) Genera 'numero_referencia' único si no existe.
        2) Guarda campos históricos de empresa y cliente.
        3) Recalcula y asigna 'total' y 'total_con_descuento' antes de guardar.
        4) Llama al super().save().
        """
        if not self.numero_referencia:
            with transaction.atomic():
                ultimo = (
                    Cotizaciones.objects
                    .annotate(n=Cast(Substr('numero_referencia', 5), IntegerField()))
                    .aggregate(maxn=Max('n'))['maxn'] or 0
                )
                self.numero_referencia = f'COT-{ultimo+1:05d}'
                
        # Guardar campos históricos del cliente
        if self.cliente and not self.cliente_nombre:
            self.cliente_nombre = self.cliente.nombre
            self.cliente_empresa = getattr(self.cliente, 'nombre_empresa', '')
            self.cliente_cuit = getattr(self.cliente, 'cuit', '')
            self.cliente_mail = getattr(self.cliente, 'mail', '')
            
        # Guardar campos históricos de la empresa  
        if self.empresa and not self.empresa_nombre:
            self.empresa_nombre = self.empresa.nombre
            self.empresa_cuit = getattr(self.empresa, 'cuit', '')
            self.empresa_mail = getattr(self.empresa, 'mail', '')
            self.empresa_telefono = getattr(self.empresa, 'telefono', '')

        super().save(*args, **kwargs)

        subtotal, _, total_con_desc = self.calcular_totales()
        self.total = subtotal
        self.total_con_descuento = total_con_desc
        super().save(update_fields=['total', 'total_con_descuento'])


class ArticulosCotizado(models.Model):
    cotizacion = models.ForeignKey(Cotizaciones, on_delete=models.CASCADE, related_name='items')
    articulo = models.ForeignKey(Articulo, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    articulo_nombre = models.CharField(max_length=30, null=True, blank=True)
    articulo_precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    articulo_descripcion = models.TextField(null=True, blank=True)
    


    @property
    def subtotal(self):
        # Usar el campo histórico en lugar del artículo original
        precio_unitario = self.articulo_precio or Decimal('0.00')
        return precio_unitario * self.cantidad
    

    def save(self, *args, **kwargs):
        if self.articulo and not self.articulo_nombre:
            self.articulo_nombre = self.articulo.nombre
            self.articulo_precio = self.articulo.precio
            self.articulo_descripcion = self.articulo.descripcion
        super().save(*args, **kwargs)