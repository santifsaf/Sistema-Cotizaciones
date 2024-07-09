from django.shortcuts import render, redirect
from .models import Cotizaciones
from .forms import CotizacionForm
from django.contrib import messages



# Create your views here.

def mis_cotizaciones(request):
    cotizaciones=Cotizaciones.objects.all()
    return render (request, "mis_cotizaciones.html", {"cotizaciones":cotizaciones}) 

def nueva_cotizacion(request):
    if request.method=="POST":
        form=CotizacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se creo una nueva cotizacion')
            return redirect('nueva_cotizacion')
        else:
            messages.error(request, 'No se pudo crear correctamente. Intentalo nuevamente')
    else:
        form=CotizacionForm()
    return render(request, "nueva_cotizacion.html", {"form":form})

