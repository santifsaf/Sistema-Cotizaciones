from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.template.loader import render_to_string
from django.http import HttpResponse
from decimal import Decimal
from cotizApp.models import Empresa
from .models import Clientes, Cotizaciones, ArticulosCotizado
from articulos.models import Articulo
from .forms import CotizacionForm
from weasyprint import HTML
from django.forms import modelformset_factory
from .models import ArticulosCotizado

ArticuloCotizadoFormSet = modelformset_factory(
    ArticulosCotizado,
    fields=('articulo', 'cantidad'),
    extra=1  
)



class MisCotizaciones(LoginRequiredMixin, ListView):
    """
    Vista para listar cotizaciones del usuario con funcionalidad de búsqueda.
    Busca por número de referencia y datos del cliente usando campos históricos.
    """
    model = Cotizaciones
    template_name = "mis_cotizaciones.html"
    context_object_name = 'cotizaciones'

    def get_queryset(self):
        search = self.request.GET.get('search')
        qs = Cotizaciones.objects.filter(usuario=self.request.user)

        if search:
            # Búsqueda por número de referencia
            cotiz_por_ref = qs.filter(numero_referencia__icontains=search)
            
            # Búsqueda en campos históricos del cliente (más confiable)
            cotiz_por_nombre_cliente = qs.filter(cliente_nombre__icontains=search)
            cotiz_por_empresa_cliente = qs.filter(cliente_empresa__icontains=search)
            cotiz_por_empresa_nombre = qs.filter(empresa_nombre__icontains=search)
            
            # Búsqueda en relaciones existentes (por compatibilidad)
            cotiz_por_cliente_rel = qs.filter(
                cliente__isnull=False,
                cliente__nombre__icontains=search
            )
            cotiz_por_empresa_rel = qs.filter(
                cliente__isnull=False,
                cliente__nombre_empresa__icontains=search
            )
            
            # Combinar todas las búsquedas
            qs = cotiz_por_ref.union(
                cotiz_por_nombre_cliente,
                cotiz_por_empresa_cliente, 
                cotiz_por_empresa_nombre,
                cotiz_por_cliente_rel,
                cotiz_por_empresa_rel
            )

        return qs

class NuevaCotizacion(LoginRequiredMixin, View):
    """Vista para crear nuevas cotizaciones con artículos asociados."""
    template_name = 'nueva_cotizacion.html'
    success_url = reverse_lazy('mis_cotizaciones')

    def _get_context_data(self, form):
        return {
            'form': form,
            'empresas': Empresa.objects.filter(usuario_log=self.request.user),
            'clientes': Clientes.objects.filter(usuario_log=self.request.user),
            'articulos_disponibles': Articulo.objects.filter(usuario_log=self.request.user),
            'fecha_actual': timezone.now().strftime('%Y-%m-%d'),
        }

    def get(self, request):
        """Renderiza formulario de nueva cotización."""
        form = CotizacionForm()
        context = self._get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Procesa el formulario de cotización y guarda los datos.
        """
        form = CotizacionForm(request.POST)
        item_forms = ArticuloCotizadoFormSet(request.POST)

        if form.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.usuario = request.user
            cotizacion.save()  

            # Guardar artículos desde las listas POST
            self._guardar_articulos(request, cotizacion)

            # Recalcular totales con los artículos recién guardados
            subtotal, _, total_con_desc = cotizacion.calcular_totales()
            cotizacion.total = subtotal
            cotizacion.total_con_descuento = total_con_desc

            # Guardar campos históricos de empresa y cliente
            if cotizacion.empresa:
                cotizacion.empresa_nombre = cotizacion.empresa.nombre
                cotizacion.empresa_cuit = cotizacion.empresa.cuit
                cotizacion.empresa_mail = cotizacion.empresa.mail
                cotizacion.empresa_telefono = cotizacion.empresa.telefono

            if cotizacion.cliente:
                cotizacion.cliente_nombre = cotizacion.cliente.nombre
                cotizacion.cliente_empresa = cotizacion.cliente.nombre_empresa
                cotizacion.cliente_cuit = cotizacion.cliente.cuit
                cotizacion.cliente_mail = cotizacion.cliente.mail

            # Guardar todos los cambios importantes
            cotizacion.save(update_fields=[
                'total', 'total_con_descuento',
                'empresa_nombre', 'empresa_cuit', 'empresa_mail', 'empresa_telefono',
                'cliente_nombre', 'cliente_empresa', 'cliente_cuit', 'cliente_mail'
            ])

            messages.success(request, f'Se creó una nueva cotización {cotizacion.numero_referencia}')
            return redirect(self.success_url)

        else:
            context = self._get_context_data(form=form)
            return render(request, self.template_name, context)
    
        

    def _guardar_articulos(self, request, cotizacion):
        """
        Guarda los artículos cotizados asociados a la cotización.
        """
        cantidades = request.POST.getlist('cantidad')
        articulos_ids = request.POST.getlist('articulos_cotizados')

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

            articulo = Articulo.objects.get(id=art_id)
            ArticulosCotizado.objects.create(
                cotizacion=cotizacion,
                articulo=articulo,
                cantidad=cantidad_val,
                articulo_nombre=articulo.nombre,
                articulo_precio=articulo.precio,
                articulo_descripcion=articulo.descripcion
            )

class EliminarCotizacion(LoginRequiredMixin, View):
    def post(self, request):
        print("POST data:", request.POST)
        accion = request.POST.get('accion')
        cotizaciones_a_eliminar = request.POST.getlist('cotizaciones_seleccionadas[]')
        print(f"Accion: {accion}, Cotizaciones a eliminar: {cotizaciones_a_eliminar}")

        if accion == 'eliminar' and cotizaciones_a_eliminar:
            Cotizaciones.objects.filter(id__in=cotizaciones_a_eliminar).delete()
            messages.success(request, 'Se eliminaron las cotizaciones seleccionadas.')
        else:
            messages.error(request, 'Debe seleccionar al menos una cotización.')
        return redirect('mis_cotizaciones')
    

def generar_pdf(request, cotizacion_id):
    """
    Genera un PDF de la cotización usando campos históricos.
    """
    try:
        cotizacion = get_object_or_404(
            Cotizaciones, 
            id=cotizacion_id, 
            usuario=request.user
        )

        articulos = cotizacion.items.all()  # Ya guarda los datos históricos

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
            
            # Datos históricos de la empresa
            "empresa_nombre": cotizacion.empresa_nombre or '-',
            "empresa_cuit": cotizacion.empresa_cuit or '-',
            "empresa_mail": cotizacion.empresa_mail or '-',
            "empresa_telefono": cotizacion.empresa_telefono or '-',
            
            # Datos históricos del cliente
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