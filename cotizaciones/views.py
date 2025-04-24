from django.shortcuts import redirect
from .models import Cotizaciones
from facturacionApp.models import Empresa
from clientes.models import Clientes
from articulos.models import Articulo
from .forms import CotizacionForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, View
from django.utils import timezone
from django.urls import reverse_lazy

# Create your views here.

class MisCotizaciones(LoginRequiredMixin, ListView):
    model = Cotizaciones
    template_name= "mis_cotizaciones.html"
    context_object_name = 'cotizaciones'


class NuevaCotizacion(LoginRequiredMixin, CreateView):
    model = Cotizaciones
    form_class = CotizacionForm
    template_name = "nueva_cotizacion.html"
    success_url = reverse_lazy("mis_cotizaciones")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Se creó una nueva cotización con ID {self.object.id}')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'No se pudo crear correctamente. Inténtalo nuevamente')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresas'] = Empresa.objects.all()
        context['clientes'] = Clientes.objects.all()
        context['articulos'] = Articulo.objects.all()  # Asegúrate de que este modelo exista

        empresa_id = self.request.GET.get('empresa')
        if empresa_id:
            context['empresa_seleccionada'] = Empresa.objects.filter(id=empresa_id).first()
        else:
            context['empresa_seleccionada'] = None

        cliente_id = self.request.GET.get('cliente')
        if cliente_id:
            context['cliente_seleccionado'] = Clientes.objects.filter(id=cliente_id).first()
        else:
            context['cliente_seleccionado'] = None

        context['fecha_actual'] = timezone.now().strftime('%Y-%m-%d')
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
    
    