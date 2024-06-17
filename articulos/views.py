from django.shortcuts import render

# Create your views here.

def mis_articulos(request):
    return render (request, "mis_articulos.html")

def nuevo_articulo(request):
    return render (request, "nuevo_articulo.html")