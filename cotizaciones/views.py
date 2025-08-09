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



class MisCotizaciones(LoginRequiredMixin, ListView):
    """
    Vista para listar cotizaciones del usuario con funcionalidad de búsqueda.
    Busca por número de referencia y datos del cliente.
    """
    model = Cotizaciones
    template_name = "mis_cotizaciones.html"
    context_object_name = 'cotizaciones'

    def get_queryset(self):
        search = self.request.GET.get('search')
        qs = Cotizaciones.objects.filter(usuario=self.request.user)

        if search:

            cotiz_por_ref = qs.filter(numero_referencia__icontains=search)
            
            cotiz_por_nombre_cliente = qs.filter(
                cliente__isnull=False,
                cliente__nombre__icontains=search
            )

            cotiz_por_empresa_cliente = qs.filter(
                cliente__isnull=False,
                cliente__nombre_empresa__icontains=search
            )
            
            qs = cotiz_por_ref.union(cotiz_por_nombre_cliente, cotiz_por_empresa_cliente)

        return qs


class NuevaCotizacion(LoginRequiredMixin, View):
    """Vista para crear nuevas cotizaciones con artículos asociados."""
    template_name = 'nueva_cotizacion.html'
    success_url = reverse_lazy('mis_cotizaciones')

    def _get_context_data(self, form):
        return {
            'form': form,
            'empresas': Empresa.objects.all(),
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
        if form.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.usuario = request.user
            cotizacion.save()  

            """Guardar artículos"""
            self._guardar_articulos(request, cotizacion)

            """Recalcular totales después de guardar los artículos"""
            cotizacion.save() 

            messages.success(request, f'Se creó una nueva cotización {cotizacion.numero_referencia}')
            return redirect(self.success_url)
        else:
            context = self._get_context_data(form)
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

            ArticulosCotizado.objects.create(
                cotizacion=cotizacion,
                articulo_id=art_id,
                cantidad=cantidad_val,
            )


class EliminarCotizacion(LoginRequiredMixin, View):
    def post(self, request):
        print("POST data:", request.POST)
        accion = request.POST.get('accion')
        cotizaciones_a_eliminar = request.POST.getlist('cotizaciones_seleccionadas[]')
        print(f"Accion: {accion}, Cotizaciones a eliminar: {cotizaciones_a_eliminar}")

        if accion == 'eliminar' and cotizaciones_a_eliminar:
            count, _ = Cotizaciones.objects.filter(id__in=cotizaciones_a_eliminar).delete()
            messages.success(request, f'Se eliminaron {count} cotización(es) correctamente.')
        else:
            messages.error(request, 'Debe seleccionar al menos una cotización o acción inválida.')
        return redirect('mis_cotizaciones')
    

def generar_pdf(request, cotizacion_id):
    """
    Genera un PDF de la cotización
    """
    try:
        cotizacion = get_object_or_404(
            Cotizaciones, 
            id=cotizacion_id, 
            usuario=request.user
        )
        
        articulos = cotizacion.items.select_related('articulo').all()
        subtotal, descuento_pct, total_con_descuento = cotizacion.calcular_totales()

        context = {
            "cotizacion": cotizacion,
            "articulos": articulos,
            "total": subtotal,  
            "total_con_descuento": total_con_descuento,  
            "descuento": float(descuento_pct) if descuento_pct else 0,
            "costo_envio": cotizacion.costo_envio or Decimal('0.00'),
            "observaciones": cotizacion.observaciones or '',
            "fecha": cotizacion.fecha,
            "numero_referencia": cotizacion.numero_referencia,
            "condiciones_pago": cotizacion.condiciones_pago,
            "empresa": cotizacion.empresa,
            "cliente": cotizacion.cliente,
        }

        html_string = render_to_string("cotizacion_pdf.html", context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'filename="cotizacion_{cotizacion.numero_referencia}.pdf"'
        return response
        
    except Exception as e:
        messages.error(request, "Error al generar el PDF. Intente nuevamente.")
        return redirect('mis_cotizaciones')