from django.urls import path
from .views import CustomLoginView, vistaRegistro
from django.urls import path
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('', vistaRegistro.as_view(), name="registro"),
    path('registration/login/', CustomLoginView.as_view(), name='login'),
        # URLs para recuperación de contraseña
    path('password-reset/', 
         CustomPasswordResetView.as_view(), 
         name='password_reset'),
    
    path('password-reset/done/', 
         CustomPasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         CustomPasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]