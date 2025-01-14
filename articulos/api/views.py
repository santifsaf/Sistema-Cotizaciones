from rest_framework import viewsets, permissions
from ..models import Articulo
from .serializers import ArticuloSerializer

class ArticuloViewSet(viewsets.ModelViewSet):
    queryset=Articulo.objects.all()
    permission_classes=[permissions.AllowAny] #############
    serializer_class=ArticuloSerializer