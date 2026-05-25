from decimal import Decimal, InvalidOperation

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr

from articulos.models import Articulo
from clientes.models import Clientes
from cotizApp.models import Empresa


class Cotizaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    condiciones_pago = models.CharField(max_length=50, null=True, blank=True)
    numero_referencia = models.CharField(unique=True, editable=False, blank=True, max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, blank=True)

    # Campos historicos de la empresa
    empresa_nombre = models.CharField(max_length=100, null=True, blank=True)
    empresa_cuit = models.CharField(max_length=20, null=True, blank=True)
    empresa_mail = models.EmailField(null=True, blank=True)
    empresa_telefono = models.CharField(max_length=20, null=True, blank=True)

    # Campos historicos del cliente
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

    class Meta:
        indexes = [
            models.Index(fields=['usuario', '-created'], name='cotiz_user_created_idx'),
            models.Index(fields=['usuario', 'numero_referencia'], name='cotiz_user_ref_idx'),
        ]

    def calcular_totales(self):
        """
        Devuelve subtotal, descuento normalizado y total con descuento.
        El costo de envio se mantiene separado para conservar el comportamiento actual.
        """
        try:
            descuento_pct = (
                Decimal(str(self.descuento).replace(",", "."))
                if self.descuento else Decimal('0.00')
            )
        except InvalidOperation:
            descuento_pct = Decimal('0.00')

        descuento_pct = max(Decimal('0.00'), min(descuento_pct, Decimal('100.00')))
        subtotal = sum(
            (item.articulo_precio or Decimal('0.00')) * item.cantidad
            for item in self.items.all()
        )
        descuento_monto = subtotal * (descuento_pct / 100)
        total_con_descuento = max(subtotal - descuento_monto, Decimal('0.00'))

        return subtotal, descuento_pct, total_con_descuento

    def asignar_datos_historicos(self):
        campos_modificados = set()

        if self.cliente and not self.cliente_nombre:
            self.cliente_nombre = self.cliente.nombre
            self.cliente_empresa = getattr(self.cliente, 'nombre_empresa', '')
            self.cliente_cuit = getattr(self.cliente, 'cuit', '')
            self.cliente_mail = getattr(self.cliente, 'mail', '')
            campos_modificados.update({
                'cliente_nombre',
                'cliente_empresa',
                'cliente_cuit',
                'cliente_mail',
            })

        if self.empresa and not self.empresa_nombre:
            self.empresa_nombre = self.empresa.nombre
            self.empresa_cuit = getattr(self.empresa, 'cuit', '')
            self.empresa_mail = getattr(self.empresa, 'mail', '')
            self.empresa_telefono = getattr(self.empresa, 'telefono', '')
            campos_modificados.update({
                'empresa_nombre',
                'empresa_cuit',
                'empresa_mail',
                'empresa_telefono',
            })

        return campos_modificados

    def actualizar_totales(self, guardar=True):
        self.total, _, self.total_con_descuento = self.calcular_totales()

        if guardar and self.pk:
            type(self).objects.filter(pk=self.pk).update(
                total=self.total,
                total_con_descuento=self.total_con_descuento,
            )

        return self.total, self.total_con_descuento

    def save(self, *args, **kwargs):
        actualizar_totales = kwargs.pop('actualizar_totales', True)

        if not self.numero_referencia:
            with transaction.atomic():
                ultimo = (
                    Cotizaciones.objects
                    .annotate(n=Cast(Substr('numero_referencia', 5), IntegerField()))
                    .aggregate(maxn=Max('n'))['maxn'] or 0
                )
                self.numero_referencia = f'COT-{ultimo + 1:05d}'

        campos_historicos = self.asignar_datos_historicos()
        update_fields = kwargs.get('update_fields')
        if update_fields is not None and campos_historicos:
            kwargs['update_fields'] = set(update_fields) | campos_historicos

        super().save(*args, **kwargs)

        if actualizar_totales:
            self.actualizar_totales(guardar=True)


class ArticulosCotizado(models.Model):
    cotizacion = models.ForeignKey(Cotizaciones, on_delete=models.CASCADE, related_name='items')
    articulo = models.ForeignKey(Articulo, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    articulo_nombre = models.CharField(max_length=30, null=True, blank=True)
    articulo_precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    articulo_descripcion = models.TextField(null=True, blank=True)

    @property
    def subtotal(self):
        precio_unitario = self.articulo_precio or Decimal('0.00')
        return precio_unitario * self.cantidad

    def save(self, *args, **kwargs):
        if self.articulo and not self.articulo_nombre:
            self.articulo_nombre = self.articulo.nombre
            self.articulo_precio = self.articulo.precio
            self.articulo_descripcion = self.articulo.descripcion
        super().save(*args, **kwargs)
