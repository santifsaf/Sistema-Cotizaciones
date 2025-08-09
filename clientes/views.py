from django.shortcuts import redirect
from .forms import ClienteForm
from .models import Clientes
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, View
from django.urls import reverse_lazy



class MisClientes(LoginRequiredMixin, ListView):
    model = Clientes
    template_name = "mis_clientes.html"
    context_object_name = "clientes"

    def get_queryset(self):
        qs = Clientes.objects.filter(usuario_log=self.request.user)
        search = self.request.GET.get('search', '').strip()
        if search:
            # Filtrar por nombre
            clientes_por_nombre = qs.filter(nombre__icontains=search)
            # Filtrar por empresa
            clientes_por_empresa = qs.filter(nombre_empresa__icontains=search)
            # Combinar ambos querysets
            qs = clientes_por_nombre.union(clientes_por_empresa)
        return qs
    
 

class NuevoCliente(LoginRequiredMixin, CreateView):
    model = Clientes
    form_class = ClienteForm
    template_name = "nuevo_cliente.html"
    success_url = reverse_lazy('mis_clientes')

    def form_valid(self, form):
        form.instance.usuario_log = self.request.user

        # Evitar duplicados: mismo nombre + usuario
        if Clientes.objects.filter(
            nombre__iexact=form.cleaned_data['nombre'].strip(),
            usuario_log=self.request.user
        ).exists():
            messages.error(self.request, "Ese cliente ya existe.")
            return redirect('nuevo_cliente')

        return super().form_valid(form)

class EliminarCliente(LoginRequiredMixin, View):
    """Permite eliminar uno o varios clientes seleccionados por el usuario."""
    def post(self, request):
        clientes_a_eliminar = request.POST.getlist('clientes_seleccionados[]')
        if clientes_a_eliminar:
            Clientes.objects.filter(id__in=clientes_a_eliminar, usuario_log=request.user).delete()
            messages.success(request, 'Se eliminaron los clientes seleccionados')
        else:
            messages.error(request, 'Debe seleccionar al menos un cliente')
        return redirect('mis_clientes')


class ActualizarCliente(LoginRequiredMixin, UpdateView):
    model=Clientes
    form_class=ClienteForm
    template_name="nuevo_cliente.html"
    success_url=reverse_lazy('mis_clientes')
    
    def get_queryset(self):
        return Clientes.objects.filter(usuario_log=self.request.user)