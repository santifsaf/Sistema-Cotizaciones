from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticuloForm
from .models import Articulo
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q



@login_required
def mis_articulos(request):
    """
    Lista artículos del usuario con funcionalidad de búsqueda.
    Busca por nombre y descripción del artículo.
    """
    search = request.GET.get('search', '').strip()
    articulos = Articulo.objects.filter(usuario_log=request.user)
    if search:
        articulos = articulos.filter(Q(nombre__icontains=search) | Q(descripcion__icontains=search))
    return render(request, "mis_articulos.html", {"articulos": articulos})

@login_required
def nuevo_articulo(request):
    """
    Muestra formulario para crear un artículo nuevo.
    Valida duplicados por nombre para el usuario.
    Guarda artículo y asigna usuario.
    """ 
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['nombre'].strip()

            # Validar duplicado
            if Articulo.objects.filter(nombre__iexact=nombre, usuario_log=request.user).exists():
                messages.error(request, 'Ya existe un artículo con ese nombre.')
                return redirect('nuevo_articulo')

            articulo = form.save(commit=False)
            articulo.usuario_log = request.user
            articulo.save()
            messages.success(request, 'El artículo fue creado correctamente.')
            return redirect('nuevo_articulo')
        else:
            messages.error(request, 'Por favor, complete correctamente los campos solicitados.')
    else:
        form = ArticuloForm()

    return render(request, 'nuevo_articulo.html', {'form': form})
        

@login_required
def eliminar_articulo(request):
    if request.method == 'POST':
        articulos_a_eliminar = request.POST.getlist('articulos_seleccionados[]')
        if articulos_a_eliminar:
            eliminados = Articulo.objects.filter(id__in=articulos_a_eliminar, usuario_log=request.user).delete()
            messages.success(request, f'Se eliminaron {eliminados[0]} artículo(s) correctamente.')
        else:
            messages.error(request, 'Debe seleccionar al menos un artículo.')
    
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