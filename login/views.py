from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy
from django.conf import settings
from allauth.account.models import EmailAddress
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

class RegistroView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Crear o conseguir EmailAddress para ese usuario y email
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
            )

            if not email_address.verified:
                print(">>> Enviando mail de confirmación para usuario:", user.email)
                email_address.send_confirmation(request)

            messages.success(
                request,
                "Te enviamos un mail de confirmacion! Por favor abrilo para validar tu cuenta. "
            )
            return redirect('login') 
        else:
            # Manejo de errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

        return render(request, "registration/registro.html", {"form": form})
    
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm  

    def form_valid(self, form):
        """
        Si el formulario es válido:
        - Inicia sesión normalmente.
        - Establece el tiempo de expiración de sesión según el campo 'remember_me':
        - Si está desmarcado: la sesión expira al cerrar el navegador.
        - Si está marcado: la sesión dura 30 días.
        """
        user = form.get_user()

        # 🚨 Chequeo si el email está confirmado
        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            messages.error(self.request, "Debes confirmar tu email antes de iniciar sesión.")
            return redirect('login')
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 30)

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Si el usuario ya está autenticado, lo redirige a la página de inicio ('home').
        Evita que vea el formulario de login si ya inició sesión.
        """
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """
    Vista para solicitar el reseteo de contraseña mediante email.

    - Muestra un mensaje genérico (por seguridad) si se envía un mail válido.
    - Usa plantillas personalizadas para el email y el HTML.
    - Usa contexto adicional para armar correctamente el link (protocolo y dominio).
    """
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    html_email_template_name = 'registration/password_reset_email.html'
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            'Si el correo electrónico está registrado, recibirás un enlace para restablecer tu contraseña.'
        )
        return super().form_valid(form)
    
    def get_email_context(self, email):
        context = super().get_email_context(email)
        context['domain'] = getattr(settings, 'DEFAULT_DOMAIN', '127.0.0.1:8000')
        context['protocol'] = getattr(settings, 'DEFAULT_PROTOCOL', 'http')
        return context



class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Vista que informa al usuario que se envió el email de recuperación (si corresponde).
    """
    template_name = 'registration/password_reset_ok.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Vista que permite al usuario establecer una nueva contraseña,
    accediendo desde el link del email recibido.
    """
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def form_valid(self, form):
        messages.success(self.request, '¡Tu contraseña ha sido cambiada exitosamente!')
        return super().form_valid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Vista final que confirma que el cambio de contraseña fue exitoso.
    """
    template_name = 'registration/password_reset_complete.html'
