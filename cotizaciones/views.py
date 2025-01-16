from django.shortcuts import redirect
from .models import Cotizaciones
from facturacionApp.models import Empresa
from clientes.models import Clientes
from .forms import CotizacionForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, View
from django.utils import timezone

# Create your views here.

class MisCotizaciones(LoginRequiredMixin, ListView):
    model = Cotizaciones
    template_name= "mis_cotizaciones.html"
    context_object_name = 'cotizaciones'


class NuevaCotizacion(LoginRequiredMixin, CreateView):
    model = Cotizaciones
    form_class=CotizacionForm 
    template_name="nueva_cotizacion.html"
    success_url="mis_cotizaciones"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Se creó una nueva cotización')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'No se pudo crear correctamente. Inténtalo nuevamente')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener todas las empresas y todos los clientes
        context['empresas'] = Empresa.objects.all()
        context['clientes'] = Clientes.objects.all()
        # context['articulos'] = Articulo.objects.all()

        # Captura la empresa seleccionada, si existe
        empresa_id = self.request.GET.get('empresa')
        if empresa_id:
            context['empresa_seleccionada'] = Empresa.objects.filter(id=empresa_id).first()
            
        # Captura el cliente seleccionado, si existe
        cliente_id = self.request.GET.get('cliente')
        if cliente_id:
            context['cliente_seleccionado'] = Clientes.objects.filter(id=cliente_id).first()

        # Captura el articulo seleccionado, si existe
        # articulo_id = self.request.GET.get('articulo')
        # if articulo_id:
        #     context['articulo_seleccionado'] = Articulo.objects.filter(id=articulo_id).first()

        fecha_actual = timezone.now().strftime('%Y-%m-%d')
        context['fecha_actual'] = fecha_actual

        return context
        


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
    
    