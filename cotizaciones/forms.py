from .models import Cotizaciones
from django import forms
from clientes.models import Clientes
from decimal import Decimal, InvalidOperation
import re


class CotizacionForm(forms.ModelForm):

    # Redefinimos como CharField para poder limpiar manualmente
    total = forms.CharField()
    total_con_descuento = forms.CharField(required=False)
    costo_envio = forms.CharField(required=False)

    class Meta:
        model = Cotizaciones
        fields = [
            'empresa',
            'cliente',
            'fecha',
            'condiciones_pago',
            'observaciones',
            'descuento',
            'costo_envio',
            'total',
            'total_con_descuento'
        ]

    def _limpiar_decimal(self, valor):
        if not valor:
            return None
        if isinstance(valor, str):
            valor = valor.strip()
            valor = re.sub(r'[^0-9,.\-]', '', valor)
            if ',' in valor and '.' in valor:
                valor = valor.replace('.', '').replace(',', '.')
            elif ',' in valor:
                valor = valor.replace(',', '.')
        try:
            return Decimal(valor)
        except (InvalidOperation, ValueError, TypeError):
            raise forms.ValidationError("Ingrese un número válido.")

    def clean_total(self):
        valor = self.cleaned_data.get('total')
        resultado = self._limpiar_decimal(valor)
        if resultado is None:
            raise forms.ValidationError("El total es obligatorio y debe ser un número válido.")
        return resultado

    def clean_total_con_descuento(self):
        valor = self.cleaned_data.get('total_con_descuento')
        resultado = self._limpiar_decimal(valor) if valor else Decimal('0.00')
        return resultado

    def clean_costo_envio(self):
        valor = self.cleaned_data.get('costo_envio')
        resultado = self._limpiar_decimal(valor) if valor else Decimal('0.00')
        return resultado

    def clean_descuento(self):
        valor = self.cleaned_data.get('descuento')
        resultado = self._limpiar_decimal(valor)
        if resultado is None:
            return Decimal('0.00')
        if resultado < 0 or resultado > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100.")
        return resultado

    def clean(self):
        cleaned = super().clean()
        total = cleaned.get('total')
        total_con_descuento = cleaned.get('total_con_descuento')

        if total is not None and total_con_descuento is not None:
            if total_con_descuento > total:
                raise forms.ValidationError("El total con descuento no puede ser mayor al total sin descuento.")
        return cleaned