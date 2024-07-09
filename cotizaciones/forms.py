from .models import Cotizaciones
from django import forms
from articulos.models import Articulo
from clientes.models import Clientes

class CotizacionForm(forms.ModelForm):
    cliente=forms.ModelMultipleChoiceField(
        queryset=Clientes.objects.all(),
        widget=forms.SelectMultiple,
        )
    
    articulos_cotizados=forms.ModelMultipleChoiceField(
        queryset=Articulo.objects.all(),
        widget=forms.SelectMultiple
    )

    class Meta:
        model=Cotizaciones
        fields=['cliente', 'articulos_cotizados']


 

