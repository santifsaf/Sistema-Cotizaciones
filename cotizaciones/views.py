from django.shortcuts import render, redirect
from .models import Cotizaciones
from .forms import CotizacionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
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

@login_required
def eliminar_cotizacion(request):
    if request.method.POST and request.POST.get('accion')=='eliminar':
        cotizaciones_a_eliminar=request.POST.get('cotizaciones_seleccionadas[]')
        if cotizaciones_a_eliminar:
            Cotizaciones.objects.filter(id__in='cotizaciones_seleccionadas[]').delete()
            messages.success(request, 'Se elimino correctamente la cotizacion seleccionada')
        else:
            messages.error(request, 'Debe seleccionar al menos una cotizacion')
        return redirect('mis_cotizaciones')
    else:
        return redirect('mis_cotizaciones')