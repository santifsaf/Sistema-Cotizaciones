from django.shortcuts import redirect, render
from facturacionApp.models import Empresa
from .models import Clientes, Cotizaciones, ArticulosCotizado
from articulos.models import Articulo
from facturacionApp.models import Empresa
from .forms import CotizacionForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy
from django.utils import timezone 
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML



# Create your views here.

class MisCotizaciones(LoginRequiredMixin, ListView):
    model = Cotizaciones
    template_name= "mis_cotizaciones.html"
    context_object_name = 'cotizaciones'


from django.views.generic import View

class NuevaCotizacion(LoginRequiredMixin, View):
    template_name = 'nueva_cotizacion.html'
    success_url = reverse_lazy('mis_cotizaciones')

    def get(self, request):
        form = CotizacionForm()
        context = {
            'form': form,
            'empresas': Empresa.objects.all(),
            'clientes': Clientes.objects.all(),
            'articulos_disponibles': Articulo.objects.all(), 
            'fecha_actual': timezone.now().strftime('%Y-%m-%d'),
            'solo_lectura': False,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cotizacion = Cotizaciones(
            usuario=request.user,
            fecha=request.POST.get('fecha'),
            condiciones_pago=request.POST.get('condiciones_pago'),
            empresa_id=request.POST.get('empresa'),
            cliente_id=request.POST.get('cliente'),
            observaciones=request.POST.get('observaciones', ''),
            descuento=Decimal(request.POST.get('descuento') or '0'),
            costo_envio=Decimal(request.POST.get('costo_envio') or '0')
        )
        cotizacion.save()  # Guardar para tener ID y poder agregar items

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

        cotizacion.total, monto_descuento, cotizacion.total_con_descuento = cotizacion.calcular_totales()
        cotizacion.save()

        messages.success(request, f'Se creó una nueva cotización con ID {cotizacion.id}')
        return redirect(self.success_url)

        


class EliminarCotizacion(LoginRequiredMixin, View):
    def post(self, request):
        if request.POST.get('accion') == 'eliminar':
            cotizaciones_a_eliminar = request.POST.getlist('cotizaciones_seleccionadas[]')
            if cotizaciones_a_eliminar:
                Cotizaciones.objects.filter(id__in=cotizaciones_a_eliminar).delete()
                messages.success(request, 'Se eliminaron correctamente las cotizaciones seleccionadas.')
            else:
                messages.error(request, 'Debe seleccionar al menos una cotización.')
        return redirect('mis_cotizaciones')
    

class GuardarCotizacion(LoginRequiredMixin, CreateView):
    model = Cotizaciones
    form_class = CotizacionForm
    template_name = 'cotizaciones/crear_cotizacion.html'
    success_url = reverse_lazy('mis_cotizaciones')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        form.save_m2m() 
        return response
    
def generar_pdf(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizaciones, id=cotizacion_id)
    articulos = cotizacion.items.all()  

    context = {
        "cotizacion": cotizacion,
        "articulos": articulos,
        "form_data": {
            "fecha": cotizacion.fecha,
            "numero_referencia": cotizacion.numero_referencia,
            "condiciones_pago": cotizacion.condiciones_pago,
            "empresa": cotizacion.empresa.id,
            "cliente": cotizacion.cliente.id,
            "descuento": cotizacion.descuento,
            "observaciones": cotizacion.observaciones or '',
        },
        "empresas": [cotizacion.empresa],
        "clientes": [cotizacion.cliente],
    }

    html_string = render_to_string("cotizacion_pdf.html", context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="cotizacion_{cotizacion.id}.pdf"'
    return response