from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .forms import EmpresaForm
from .models import Empresa
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class Home(TemplateView):
    """Vista de la página principal."""
    template_name = "home.html"

@login_required
def mis_empresas(request):
    """
    Muestra la lista de empresas registradas.
    Solo accesible para usuarios autenticados.
    """
    empresas = Empresa.objects.filter(usuario_log=request.user)  
    return render(request, "mis_empresas.html", {"empresas": empresas})

@login_required
def nueva_empresa(request):
    """
    Permite crear una nueva empresa.
    Si el método es POST, valida y guarda el formulario.
    Si no, muestra el formulario vacío.
    """
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False) 
            empresa.usuario_log = request.user 
            empresa.save() 
            messages.success(request, 'La empresa fue creada correctamente.')
            return redirect('mis_empresas')
        else:
            messages.error(request, 'Por favor, complete correctamente los campos solicitados.')
    else:
        form = EmpresaForm()
    return render(request, 'nueva_empresa.html', {'form': form})

@login_required
def eliminar_empresa(request):
    """
    Elimina empresas seleccionadas desde la lista.
    Solo accesible por POST y si se seleccionaron empresas.
    """
    if request.method == 'POST' and request.POST.get('accion') == 'eliminar':
        empresas_a_eliminar = request.POST.getlist('empresas_seleccionadas[]')
        if empresas_a_eliminar:
            Empresa.objects.filter(id__in=empresas_a_eliminar,usuario_log=request.user).delete()
            messages.success(request, 'Las empresas seleccionadas se han eliminado correctamente.')
        else:
            messages.error(request, 'Debe seleccionar al menos una empresa.')
        return redirect('mis_empresas')
    return redirect('mis_empresas')

@login_required
def actualizar_empresa(request, empresa_id):
    """
    Permite editar los datos de una empresa existente.
    Si el método es POST, valida y guarda los cambios.
    Si no, muestra el formulario con los datos actuales.
    """
    empresa = get_object_or_404(Empresa, id=empresa_id, usuario_log=request.user)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'La empresa se ha actualizado correctamente.')
            return redirect('mis_empresas')
        else:
            messages.error(request, 'Hubo un error al actualizar la empresa.')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'nueva_empresa.html', {'form': form, 'empresa': empresa})