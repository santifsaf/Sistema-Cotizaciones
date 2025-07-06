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
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CotizacionForm(request.POST)
        if form.is_valid():
            print("DEBUG descuento en form.cleaned_data:", form.cleaned_data.get('descuento'))
            cotizacion = form.save(commit=False)
            cotizacion.usuario = request.user
            cotizacion.save()  # Guardamos para tener ID y FK

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

            # Recalcular totales y actualizar sólo total y total_con_descuento
            total, _, total_con_descuento = cotizacion.calcular_totales()
            cotizacion.total = total
            cotizacion.total_con_descuento = total_con_descuento or Decimal('0.00')

            cotizacion.save()

            messages.success(request, f'Se creó una nueva cotización con ID {cotizacion.id}')
            return redirect(self.success_url)
        else:
            context = {
                'form': form,
                'empresas': Empresa.objects.all(),
                'clientes': Clientes.objects.all(),
                'articulos_disponibles': Articulo.objects.all(),
                'fecha_actual': timezone.now().strftime('%Y-%m-%d'),
                
            }
            print("Errores del formulario:", form.errors)
            return render(request, self.template_name, context)


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
    
def generar_pdf(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizaciones, id=cotizacion_id)
    articulos = cotizacion.items.all()

    total, descuento, total_con_descuento = cotizacion.calcular_totales()

    context = {
        "cotizacion": cotizacion,
        "articulos": articulos,
        "total": total,
        "total_con_descuento": total_con_descuento,
        "descuento": float(descuento) if descuento else 0,
        "costo_envio": cotizacion.costo_envio or Decimal('0.00'),
        # Si usás otros campos, agregalos acá directo del modelo
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
    response['Content-Disposition'] = f'filename="cotizacion_{cotizacion.id}.pdf"'
    return response