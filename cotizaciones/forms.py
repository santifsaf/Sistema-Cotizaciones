from .models import Cotizaciones, ArticulosCotizado
from django import forms
from clientes.models import Clientes


class CotizacionForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        widget=forms.Select
    )


    class Meta:
        model = Cotizaciones
        fields = ['empresa','cliente', 'fecha', 'condiciones_pago', 'observaciones', 'descuento','costo_envio']


