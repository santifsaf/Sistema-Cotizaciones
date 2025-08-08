from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica la clase form-control a todos los campos automáticamente
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        
        # Eliminar mensajes de ayuda por defecto
        for name in ['username', 'password1', 'password2']:
            self.fields[name].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    
    def clean_email(self):
        # No revelamos si el email existe o no por seguridad
        return self.cleaned_data.get('email').strip().lower()
