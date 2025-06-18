from .models import Cotizaciones
from django import forms
from articulos.models import Articulo
from clientes.models import Clientes

class CotizacionForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        widget=forms.Select
    )
    articulos_cotizados = forms.ModelMultipleChoiceField(
        queryset=Articulo.objects.all(),
        widget=forms.SelectMultiple(attrs={'name': 'articulo'})  
    )

    class Meta:
        model = Cotizaciones
        fields = ['cliente', 'articulos_cotizados', 'fecha', 'condiciones_pago', 'observaciones']


 

