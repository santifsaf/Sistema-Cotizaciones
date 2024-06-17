from django.db import models

# Create your models here.

class Cotizaciones(models.Model):
    numero_referencia=models.IntegerField(unique=True, editable=False)
    cliente=models.CharField(max_length=50)
    total_cotizado=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs): 
        if not self.id:
            self.referencia = f'COT-{self.id}'
        super().save(*args, **kwargs)
 
    class Meta:
        verbose_name="Cotizacion"
        verbose_name_plural="Cotizaciones"
    
    def __str__(self):
     return self.numero_referencia