from django.urls import path
from .views import CustomLoginView, vistaRegistro

urlpatterns = [
    path('', vistaRegistro.as_view(), name="registro"),
    path('registration/login/', CustomLoginView.as_view(), name='login'),
    ]