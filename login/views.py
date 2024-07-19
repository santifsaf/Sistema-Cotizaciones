from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Formulario de django 
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView
# Create your views here.

class vistaRegistro(View):
    def get(self, request):  #Encargada de crear el formulario
        form=UserCreationForm()
        return render(request, "registration/registro.html",{"form":form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
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