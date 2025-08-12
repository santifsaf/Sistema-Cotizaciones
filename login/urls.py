from django.urls import path
from .views import CustomLoginView, RegistroView
from django.contrib.auth.views import LogoutView
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path('', RegistroView.as_view(), name="registro"),
    path('registration/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

     # URLs para recuperación de contraseña
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]