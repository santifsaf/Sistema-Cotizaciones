from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, View
from weasyprint import HTML

from articulos.models import Articulo
from clientes.models import Clientes
from cotizApp.models import Empresa
from .forms import CotizacionForm
from .models import ArticulosCotizado, Cotizaciones


class MisCotizaciones(LoginRequiredMixin, ListView):
    """
    Lista cotizaciones del usuario con busqueda por referencia y datos historicos.
    """
    model = Cotizaciones
    template_name = "mis_cotizaciones.html"
    context_object_name = 'cotizaciones'

    def get_queryset(self):
        search = self.request.GET.get('search')
        qs = Cotizaciones.objects.filter(usuario=self.request.user).order_by('-created')

        if search:
            qs = qs.filter(
                Q(numero_referencia__icontains=search)
                | Q(cliente_nombre__icontains=search)
                | Q(cliente_empresa__icontains=search)
                | Q(empresa_nombre__icontains=search)
            )

        return qs


class NuevaCotizacion(LoginRequiredMixin, View):
    """Crea cotizaciones con articulos asociados."""
    template_name = 'nueva_cotizacion.html'
    success_url = reverse_lazy('mis_cotizaciones')
    DESCUENTO_EFECTIVO = Decimal('0.90')

    def _get_context_data(self, form):
        return {
            'form': form,
            'empresas': Empresa.objects.filter(usuario_log=self.request.user),
            'clientes': Clientes.objects.filter(usuario_log=self.request.user),
            'articulos_disponibles': Articulo.objects.filter(usuario_log=self.request.user),
            'fecha_actual': timezone.now().strftime('%Y-%m-%d'),
        }

    def get(self, request):
        form = CotizacionForm(user=request.user)
        context = self._get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = CotizacionForm(request.POST, user=request.user)

        if form.is_valid():
            with transaction.atomic():
                cotizacion = form.save(commit=False)
                cotizacion.usuario = request.user
                cotizacion.save(actualizar_totales=False)

                articulos_guardados = self._guardar_articulos(request, cotizacion)
                if articulos_guardados == 0:
                    cotizacion.delete()
                    messages.error(request, 'Debe seleccionar al menos un articulo valido.')
                    context = self._get_context_data(form=form)
                    return render(request, self.template_name, context)

                cotizacion.actualizar_totales(guardar=True)

            messages.success(request, f'Se creo una nueva cotizacion {cotizacion.numero_referencia}')
            return redirect(self.success_url)

        context = self._get_context_data(form=form)
        return render(request, self.template_name, context)

    def _guardar_articulos(self, request, cotizacion):
        cantidades = request.POST.getlist('cantidad')
        articulos_ids = request.POST.getlist('articulos_cotizados')
        articulos_guardados = 0
        ids_validos = []

        for art_id in articulos_ids:
            try:
                ids_validos.append(int(art_id))
            except (TypeError, ValueError):
                continue

        articulos_map = Articulo.objects.filter(
            id__in=ids_validos,
            usuario_log=request.user,
        ).in_bulk()

        for i in range(len(articulos_ids)):
            art_id = articulos_ids[i].strip()
            if not art_id:
                continue

            try:
                cantidad_val = int(cantidades[i])
                if cantidad_val <= 0:
                    continue
            except (IndexError, ValueError):
                continue

            try:
                articulo_id = int(art_id)
            except ValueError:
                continue

            articulo = articulos_map.get(articulo_id)
            if articulo is None:
                continue

            ArticulosCotizado.objects.create(
                cotizacion=cotizacion,
                articulo=articulo,
                cantidad=cantidad_val,
                articulo_nombre=articulo.nombre,
                articulo_precio=self._precio_por_condicion_pago(articulo, cotizacion),
                articulo_descripcion=articulo.descripcion,
            )
            articulos_guardados += 1

        return articulos_guardados

    def _precio_por_condicion_pago(self, articulo, cotizacion):
        precio = Decimal(str(articulo.precio or 0))
        if cotizacion.condiciones_pago == 'Efectivo':
            return precio * self.DESCUENTO_EFECTIVO
        return precio


class EliminarCotizacion(LoginRequiredMixin, View):
    def post(self, request):
        accion = request.POST.get('accion')
        cotizaciones_a_eliminar = request.POST.getlist('cotizaciones_seleccionadas[]')

        if accion == 'eliminar' and cotizaciones_a_eliminar:
            Cotizaciones.objects.filter(
                id__in=cotizaciones_a_eliminar,
                usuario=request.user,
            ).delete()
            messages.success(request, 'Se eliminaron las cotizaciones seleccionadas.')
        else:
            messages.error(request, 'Debe seleccionar al menos una cotizacion.')
        return redirect('mis_cotizaciones')


@login_required
def generar_pdf(request, cotizacion_id):
    """
    Genera un PDF de la cotizacion usando campos historicos.
    """
    try:
        cotizacion = get_object_or_404(
            Cotizaciones.objects.prefetch_related('items'),
            id=cotizacion_id,
            usuario=request.user,
        )

        articulos = cotizacion.items.all()

        context = {
            "cotizacion": cotizacion,
            "articulos": articulos,
            "total": cotizacion.total,
            "total_con_descuento": cotizacion.total_con_descuento,
            "descuento": float(cotizacion.descuento or 0),
            "costo_envio": cotizacion.costo_envio or Decimal('0.00'),
            "observaciones": cotizacion.observaciones or '',
            "fecha": cotizacion.fecha,
            "numero_referencia": cotizacion.numero_referencia,
            "condiciones_pago": cotizacion.condiciones_pago or '',
            "empresa_nombre": cotizacion.empresa_nombre or '-',
            "empresa_cuit": cotizacion.empresa_cuit or '-',
            "empresa_mail": cotizacion.empresa_mail or '-',
            "empresa_telefono": cotizacion.empresa_telefono or '-',
            "cliente_nombre": cotizacion.cliente_nombre or '-',
            "cliente_empresa": cotizacion.cliente_empresa or '-',
            "cliente_cuit": cotizacion.cliente_cuit or '-',
            "cliente_mail": cotizacion.cliente_mail or '-',
        }

        html_string = render_to_string("cotizacion_pdf.html", context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="cotizacion_{cotizacion.numero_referencia}.pdf"'
        return response

    except Exception:
        messages.error(request, "Error al generar el PDF. Intente nuevamente.")
        return redirect('mis_cotizaciones')
