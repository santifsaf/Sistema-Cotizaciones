from django.shortcuts import render, redirect
from .forms import ArticuloForm
from .models import Articulo
from django.contrib import messages


# Create your views here.

def mis_articulos(request):
    articulos=Articulo.objects.all()
    return render(request, "mis_articulos.html", {"articulos": articulos}) 

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
        