from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpresaForm
from .models import Empresa
from django.contrib import messages
from django.contrib.auth.decorators import login_required



class Home(TemplateView):
    template_name="home.html"


@login_required
def mis_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, "mis_empresas.html", {"empresas": empresas})


@login_required
def nueva_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)  
        if form.is_valid():
            form.save()
            messages.success(request, 'La empresa fue creada correctamente.')
            return redirect('mis_empresas')  # Redirige a la lista de empresas después de guardar
        else:
            messages.error(request, 'Por favor, complete correctamente los campos solicitados.')
    else:
        form = EmpresaForm()

    return render(request, 'nueva_empresa.html', {'form': form})



@login_required
def eliminar_empresa(request):
    if request.method == 'POST' and request.POST.get('accion') == 'eliminar':
        empresas_a_eliminar = request.POST.getlist('empresas_seleccionadas[]')
        if empresas_a_eliminar:
            Empresa.objects.filter(id__in=empresas_a_eliminar).delete()
            messages.success(request, 'Las empresas seleccionadas se han eliminado correctamente.')
        else:
            messages.error(request, 'Debe seleccionar al menos una empresa.')

        return redirect('mis_empresas')
    else:
        return redirect('mis_empresas')

@login_required
def actualizar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)

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