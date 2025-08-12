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
            return  # Si no hay email, nada que hacer

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return  # Usuario nuevo, sigue el flujo normal

        # Usuario existente: conectar cuenta social y login sin mail confirm
        sociallogin.connect(request, user)
        perform_login(request, user, email_verification='optional')
        request.session['next'] = reverse('home')

    def get_login_redirect_url(self, request):
        return request.session.pop('next', super().get_login_redirect_url(request))

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        email = user.email
        if email:
            # Marcamos email como verificado para evitar mail de confirmación
            EmailAddress.objects.update_or_create(
                user=user,
                email=email,
                defaults={'verified': True, 'primary': True}
            )
        return user