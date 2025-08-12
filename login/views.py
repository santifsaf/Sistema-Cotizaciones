from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)


User = get_user_model()

class RegistroView(View):
    """
    Registro manual con validación de email.
    Si el email ya existe y está verificado -> bloquea registro.
    Si existe pero no está verificado -> sobrescribe usuario y envía confirmación.
    """

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/registro.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Caso 1: Email ya verificado
            if EmailAddress.objects.filter(email__iexact=email, verified=True).exists():
                messages.error(
                    request,
                    "Este email ya está registrado y verificado. Iniciá sesión con tu cuenta."
                )
                return render(request, "registration/registro.html", {"form": form})

            # Caso 2: Email no verificado pero existente
            try:
                user = User.objects.get(email__iexact=email)
                user.username = form.cleaned_data.get('username')  # Actualiza datos si querés
                user.set_password(form.cleaned_data.get('password1'))
                user.is_active = False
                user.save()
            except User.DoesNotExist:
                # Usuario nuevo
                user = form.save(commit=False)
                user.is_active = False
                user.save()

            # EmailAddress sincronizado
            email_address, created = EmailAddress.objects.get_or_create(user=user)
            if email_address.email != user.email:
                email_address.email = user.email
                email_address.save()

            # Enviar confirmación con EmailConfirmationHMAC
            confirmation = EmailConfirmationHMAC(email_address)
            confirmation.send(request)

            messages.success(
                request,
                "Te enviamos un mail de confirmación. Por favor, abrilo para validar tu cuenta."
            )
            return redirect('login')

        # Errores de formulario
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(request, f"{error}")
                else:
                    label = form.fields[field].label or field
                    messages.error(request, f"{label}: {error}")

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

        # Chequeo si el email está confirmado
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

