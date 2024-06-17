from django.shortcuts import render

# Create your views here.

def mis_cotizaciones(request):
    return render (request, "mis_cotizaciones.html") 

def nueva_cotizacion(request):
    return render (request, "nueva_cotizacion.html") 