from django.shortcuts import render

# Create your views here.

def mis_clientes(request):
    return render (request, "mis_clientes.html")

def nuevo_cliente(request):
    return render (request, "mis_clientes.html")