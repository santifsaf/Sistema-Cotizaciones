from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from decimal import Decimal

from articulos.models import Articulo
from clientes.models import Clientes
from cotizApp.models import Empresa
from .forms import CotizacionForm
from .models import ArticulosCotizado, Cotizaciones


@override_settings(SECURE_SSL_REDIRECT=False)
class PruebasCotizaciones(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='usuario_uno',
            email='uno@example.com',
            password='pass-test-123',
        )
        self.other_user = User.objects.create_user(
            username='usuario_dos',
            email='dos@example.com',
            password='pass-test-123',
        )

        self.empresa = Empresa.objects.create(
            usuario_log=self.user,
            nombre='Empresa Uno',
            cuit='20-11111111-1',
            telefono='1111-1111',
            mail='empresa1@example.com',
        )
        self.other_empresa = Empresa.objects.create(
            usuario_log=self.other_user,
            nombre='Empresa Dos',
            cuit='20-22222222-2',
            telefono='2222-2222',
            mail='empresa2@example.com',
        )

        self.cliente = Clientes.objects.create(
            usuario_log=self.user,
            nombre='Cliente Uno',
            nombre_empresa='Cliente Empresa Uno',
            cuit='30-11111111-1',
            telefono='3333-3333',
            mail='cliente1@example.com',
        )
        self.other_cliente = Clientes.objects.create(
            usuario_log=self.other_user,
            nombre='Cliente Dos',
            nombre_empresa='Cliente Empresa Dos',
            cuit='30-22222222-2',
            telefono='4444-4444',
            mail='cliente2@example.com',
        )

        self.other_articulo = Articulo.objects.create(
            usuario_log=self.other_user,
            nombre='Articulo Ajeno',
            descripcion='No pertenece al usuario logueado',
            precio=100,
        )
        self.articulo = Articulo.objects.create(
            usuario_log=self.user,
            nombre='Articulo Propio',
            descripcion='Pertenece al usuario logueado',
            precio=150,
        )

    def test_eliminar_solo_borra_cotizaciones_del_usuario(self):
        own_cotizacion = Cotizaciones.objects.create(usuario=self.user)
        other_cotizacion = Cotizaciones.objects.create(usuario=self.other_user)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('eliminar_cotizacion'),
            {
                'accion': 'eliminar',
                'cotizaciones_seleccionadas[]': [str(other_cotizacion.id)],
            },
        )

        self.assertRedirects(response, reverse('mis_cotizaciones'))
        self.assertTrue(Cotizaciones.objects.filter(id=own_cotizacion.id).exists())
        self.assertTrue(Cotizaciones.objects.filter(id=other_cotizacion.id).exists())

    def test_formulario_rechaza_empresa_y_cliente_ajenos(self):
        form = CotizacionForm(
            data={
                'empresa': self.other_empresa.id,
                'cliente': self.other_cliente.id,
                'total': '100.00',
            },
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn('empresa', form.errors)
        self.assertIn('cliente', form.errors)

    def test_creacion_ignora_articulos_ajenos(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('nueva_cotizacion'),
            {
                'empresa': self.empresa.id,
                'cliente': self.cliente.id,
                'fecha': '2026-05-25',
                'condiciones_pago': 'Efectivo',
                'descuento': '0',
                'costo_envio': '0',
                'total': '100.00',
                'total_con_descuento': '100.00',
                'cantidad': ['1'],
                'articulos_cotizados': [str(self.other_articulo.id)],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cotizaciones.objects.filter(usuario=self.user).exists())
        self.assertFalse(
            ArticulosCotizado.objects.filter(
                cotizacion__usuario=self.user,
                articulo=self.other_articulo,
            ).exists()
        )

    def test_creacion_con_efectivo_aplica_descuento_y_guarda_item(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('nueva_cotizacion'),
            {
                'empresa': self.empresa.id,
                'cliente': self.cliente.id,
                'fecha': '2026-05-25',
                'condiciones_pago': 'Efectivo',
                'descuento': '10',
                'costo_envio': '0',
                'total': '270.00',
                'total_con_descuento': '243.00',
                'cantidad': ['2'],
                'articulos_cotizados': [str(self.articulo.id)],
            },
        )

        self.assertRedirects(response, reverse('mis_cotizaciones'))
        cotizacion = Cotizaciones.objects.get(usuario=self.user)
        self.assertEqual(cotizacion.items.count(), 1)
        item = cotizacion.items.get()
        self.assertEqual(item.articulo_precio, Decimal('135.00'))
        self.assertEqual(cotizacion.total, Decimal('270.00'))
        self.assertEqual(cotizacion.total_con_descuento, Decimal('243.00'))
        self.assertEqual(cotizacion.empresa_nombre, self.empresa.nombre)
        self.assertEqual(cotizacion.cliente_nombre, self.cliente.nombre)

    def test_creacion_con_precio_de_lista_mantiene_precio_original(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('nueva_cotizacion'),
            {
                'empresa': self.empresa.id,
                'cliente': self.cliente.id,
                'fecha': '2026-05-25',
                'condiciones_pago': 'Precio de lista',
                'descuento': '0',
                'costo_envio': '0',
                'total': '300.00',
                'total_con_descuento': '300.00',
                'cantidad': ['2'],
                'articulos_cotizados': [str(self.articulo.id)],
            },
        )

        self.assertRedirects(response, reverse('mis_cotizaciones'))
        cotizacion = Cotizaciones.objects.get(usuario=self.user)
        item = cotizacion.items.get()
        self.assertEqual(item.articulo_precio, Decimal('150.00'))
        self.assertEqual(cotizacion.total, Decimal('300.00'))
        self.assertEqual(cotizacion.total_con_descuento, Decimal('300.00'))
