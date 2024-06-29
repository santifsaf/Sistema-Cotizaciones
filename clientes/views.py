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

def eliminar_cliente(request):
    if request.method == 'POST' and request.POST.get('accion') == 'eliminar':
        clientes_a_eliminar = request.POST.getlist('clientes_seleccionados[]')
        if clientes_a_eliminar:
            try:
                cli=Clientes.objects.filter(id__in=clientes_a_eliminar).delete()
            except Clientes.DoesNotExist:
                pass

            messages.success(request, 'Se eliminaron los clientes seleccionados')    
        else:
            messages.error(request, 'Debe seleccionar al menos un cliente')
        return redirect('mis_clientes')
    else:
        return redirect('mis_clientes')

            
def actualizar_cliente(request, cliente_id):
    cliente=Clientes.objects.get(id=cliente_id)
    if request.method=='POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'El cliente se actualizo correctamente')
            return redirect('mis_clientes')
        else:
            messages.error(request, 'Hubo un error al actualizar el cliente')
    else:
        form= ClienteForm(instance=cliente)
    
    return render(request, 'actualizar_cliente.html', {'form':form, 'cliente':cliente})
