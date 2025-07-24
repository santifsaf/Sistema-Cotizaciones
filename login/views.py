from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib import messages

class vistaRegistro(View):
    def get(self, request):
        form = CustomUserCreationForm()  # Usa el formulario personalizado
        return render(request, "registration/registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(request, "registration/registro.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm  
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Si el usuario no quiere ser recordado, la sesión expirará al cerrar el navegador
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            'Si el correo electrónico está registrado, recibirás un enlace para restablecer tu contraseña.'
        )
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def form_valid(self, form):
        messages.success(self.request, '¡Tu contraseña ha sido cambiada exitosamente!')
        return super().form_valid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
