from django.shortcuts import render, redirect
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
        return Clientes.objects.filter(usuario_log=self.request.user)
    
 

class NuevoCliente(LoginRequiredMixin, CreateView):
    model= Clientes
    form_class=ClienteForm
    template_name="nuevo_cliente.html"
    success_url=reverse_lazy('mis_clientes')

    def form_valid(self, form):
        form.instance.usuario_log = self.request.user 
        return super().form_valid(form)

class EliminarCliente(LoginRequiredMixin, View):
    def post(self, request):
        if request.method == 'POST' and request.POST.get('accion')=='eliminar':
            clientes_a_eliminar=request.POST.getlist('clientes_seleccionados[]')
            if clientes_a_eliminar:
                Clientes.objects.filter(id__in=clientes_a_eliminar, usuario_log=request.user).delete()
                messages.success(request, 'Se eliminaron los clientes seleccionados')
            else:
                messages.error(request, 'Debe seleccionar al menos un cliente')
            
            return redirect('mis_clientes')
        else:
            return redirect('mis_clientes')


class ActualizarCliente(LoginRequiredMixin, UpdateView):
    model=Clientes
    form_class=ClienteForm
    template_name="nuevo_cliente.html"
    success_url=reverse_lazy('mis_clientes')
    
    def get_queryset(self):
        return Clientes.objects.filter(usuario_log=self.request.user)