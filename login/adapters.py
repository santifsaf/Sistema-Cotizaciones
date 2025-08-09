from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.urls import reverse
from allauth.account.utils import perform_login

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return  # Si el proveedor no devuelve email, no hacemos nada

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return  # No existe el usuario, allauth seguirá su flujo normal

        # Si el usuario existe, conectamos la cuenta social
        sociallogin.connect(request, user)

        # Logueamos sin exigir verificación de email
        perform_login(request, user, email_verification='optional')

        # Guardamos la URL de redirección en sesión
        request.session['next'] = reverse('home')
    
    def get_login_redirect_url(self, request):
        """
        Si guardamos una redirección en `pre_social_login`,
        aquí la usamos para enviar al usuario a la página deseada.
        """
        return request.session.pop('next', super().get_login_redirect_url(request))
