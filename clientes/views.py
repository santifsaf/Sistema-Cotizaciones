from django.shortcuts import render, redirect
from .forms import ClienteForm
from .models import Clientes
from django.contrib import messages


# Create your views here.

def mis_clientes(request):
    clientes=Clientes.objects.all()
    return render(request, "mis_clientes.html", {"clientes": clientes})
 

def nuevo_cliente(request):
    if request.method=='POST':
        form=ClienteForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, 'El cliente fue agregado correctamente.')
            return redirect('nuevo_cliente')
        else:
            messages.error(request, 'Ingrese los datos de cliente correctamente.')
    else:
        form=ClienteForm()

        
    return render (request, "nuevo_cliente.html", {'form':form})