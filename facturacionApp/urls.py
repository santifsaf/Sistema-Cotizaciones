from django.urls import path
from . import views
from .views import exit

urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', exit, name="exit")
]
