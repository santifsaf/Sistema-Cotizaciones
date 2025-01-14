from rest_framework import serializers
from..models import Clientes

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Clientes
        fields='__all__'
        read_only_fields=('id','created','updated')
        