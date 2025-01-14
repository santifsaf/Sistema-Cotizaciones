from rest_framework import serializers
from ..models import Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model=Articulo
        fields='__all__'
        read_only_fields=('id','created','updated')