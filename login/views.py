from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm  #Formulario de django 
from django.contrib.auth import login
from django.contrib import messages
# Create your views here.

class vistaRegistro(View):
    def get(self, request):  #Encargada de crear el formulario
        form=UserCreationForm()
        return render(request, "registration/registro.html",{"form":form})

    def post(self, request): #Envio de informacion a traves del formuilario 
        form=UserCreationForm(request.POST)

        if form.is_valid():

            usuario=form.save() #Almacenamos la informacion del formulario. Con la instruccion save() se almacena el usuario y la contraseña en la base de datos
            login(request, usuario)
        else:
            for msj in form.error_messages:
                messages.error(request, form.error_messages[msj])
        return render(request, "registration/registro.html",{"form":form})
