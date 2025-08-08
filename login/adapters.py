from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Si ya existe un usuario con ese email conectamos el sociallogin
            sociallogin.connect(request, user)
            # Forzamos login automático sin pasar por signup
            from allauth.account.utils import perform_login
            perform_login(request, user, email_verification='optional')
            # Redirigir a home o a donde quieras
            return redirect(reverse('home'))
