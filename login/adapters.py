from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.urls import reverse
from allauth.account.utils import perform_login
from allauth.account.models import EmailAddress

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return  # No existe, sigue el flujo normal

        # Loguear al usuario existente SIN pasar por verificación
        perform_login(request, user, email_verification='optional', redirect_url=reverse('home'))

        # Cancelamos el flujo normal para evitar crear otro usuario o pasar por confirmación
        sociallogin.state['process'] = 'login'

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        email = user.email
        if email:
            EmailAddress.objects.update_or_create(
                user=user,
                email=email,
                defaults={'verified': True, 'primary': True}
            )
        return user