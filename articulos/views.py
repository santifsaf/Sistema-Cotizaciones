from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticuloForm
from .models import Articulo
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def mis_articulos(request):
    """
    Lista artículos del usuario con funcionalidad de búsqueda.
    Busca en nombre y descripción del artículo.
    """
    search = request.GET.get('search', '').strip()
    articulos = Articulo.objects.filter(usuario_log=request.user)
    if search:
        # Filtrar por nombre
        articulos_por_nombre = articulos.filter(nombre__icontains=search)
        # Filtrar por descripción
        articulos_por_descripcion = articulos.filter(descripcion__icontains=search)
        # Combinar ambos querysets
        articulos = articulos_por_nombre.union(articulos_por_descripcion)
    return render(request, "mis_articulos.html", {"articulos": articulos})

@login_required
def nuevo_articulo(request):
    if request.method == 'POST':
        form=ArticuloForm(request.POST, request.FILES)
        if form.is_valid(): 
            Articulo=form.save(commit=False)
            Articulo.usuario_log=request.user
            Articulo.save()
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
            Articulo.objects.filter(id__in=articulos_a_eliminar, usuario_log=request.user).delete()
            messages.success(request, 'Los artículos seleccionados se han eliminado correctamente.')
        else:
            messages.error(request, 'Debe seleccionar al menos un artículo.')

        return redirect('mis_articulos')
    else:
        return redirect('mis_articulos')
    

@login_required
def actualizar_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id, usuario_log=request.user)

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