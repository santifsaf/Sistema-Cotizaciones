from django.shortcuts import render, redirect
from django.views.generic import View #Para crear vistas basadas en clases
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Formularios creacion y autenticacion 
from django.contrib.auth import login  
from django.contrib import messages
from django.contrib.auth.views import LoginView #vista basad en clases para el inicio de sesion.  
# Create your views here.

class vistaRegistro(View):
    def get(self, request):   #solicitud get al cargar la pagina
        form=UserCreationForm() #Creamos una instancia vacia del formulario
        return render(request, "registration/registro.html",{"form":form}) #renderizamos el template y pasamos el form al contexto 

    def post(self, request): #solicitud post al enviar el formulario 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) #inicia sesion con el nuevo usuario
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return render(request, "registration/registro.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm