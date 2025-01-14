from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticuloForm
from .models import Articulo
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def mis_articulos(request):
    articulos=Articulo.objects.all()
    return render(request, "mis_articulos.html", {"articulos": articulos}) 

@login_required
def nuevo_articulo(request):
    if request.method == 'POST':
        form=ArticuloForm(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            messages.success(request, 'El articulo fue creado correctamente.')
            return redirect('nuevo_articulo')
        else:
            messages.error(request, 'Por favor, complete correctamente los campos solicitados.')
    else:
        form=ArticuloForm()

    return render(request, 'nuevo_articulo.html', {'form': form})
        

@login_required
def eliminar_articulo(request):
    if request.method == 'POST' and request.POST.get('accion') == 'eliminar':
        articulos_a_eliminar = request.POST.getlist('articulos_seleccionados[]')
        if articulos_a_eliminar:
            Articulo.objects.filter(id__in=articulos_a_eliminar).delete()
            messages.success(request, 'Los artículos seleccionados se han eliminado correctamente.')
        else:
            messages.error(request, 'Debe seleccionar al menos un artículo.')

        return redirect('mis_articulos')
    else:
        return redirect('mis_articulos')
    

@login_required
def actualizar_articulo(request, articulo_id):
    articulo = Articulo.objects.get(id=articulo_id)

    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'El artículo se ha actualizado correctamente.')
            return redirect('mis_articulos')
        else:
            messages.error(request, 'Hubo un error al actualizar el artículo.')
    else:
        form = ArticuloForm(instance=articulo)

    return render(request, 'nuevo_articulo.html', {'form': form, 'articulo': articulo})