from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(SECURE_SSL_REDIRECT=False)
class PruebasLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='usuario_login',
            email='login@example.com',
            password='pass-test-123',
        )
        self.email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            primary=True,
            verified=False,
        )

    def test_login_con_email_verificado(self):
        self.email_address.verified = True
        self.email_address.save()

        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'pass-test-123',
        })

        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.id))

    def test_login_rechaza_email_sin_verificar(self):
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': 'pass-test-123',
        })

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)
