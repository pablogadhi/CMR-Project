from django.db import models
from django.urls import reverse

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    activo = models.BooleanField(default=True)
    nombre = models.CharField(max_length=50, null=True)
    TIPOSEXO = (
        ('femenino', 'f'),
        ('masculino', 'm'),
        cualquiercosa
    )
    sexo = models.CharField(max_length=8, choices=TIPOSEXO, blank=True, default='f')
    edad = models.IntegerField(default=0)
    telefono = models.IntegerField(default=0)
    mail = models.EmailField(null=True)
    fechaInicio = models.DateField(null=True)
    TIPOREP = (
        ('buena', 'b'),
        ('normal', 'n'),
        ('mala', 'm'),
    )
    reputacion = models.CharField(max_length=6, choices=TIPOREP, blank=True, default='b')
    foto = models.ImageField(null=True)
    def __str__(self):
       return self.nombre

    def get_absolute_url(self):
        return reverse('detalle-cliente',args=[str(self.id)])
    
    class Meta:
        abstract = True

class Propiedad(models.Model):
    id = models.AutoField(primary_key=True)
    propietario = models.ForeignKey('Propietario', on_delete=models.CASCADE, default=0)
    intermediario = models.ForeignKey('Intermediario', on_delete=models.CASCADE, default=0)
    direccion = models.CharField(max_length=50, null=True)
    valuacion = models.FloatField(default=0.0)
    tipo = models.CharField(max_length=20, default="casa")
    informacion = models.CharField(max_length=500, null=True)
    foto = models.ImageField(null=True)
    tamano = models.DecimalField(decimal_places=2, max_digits=8, default=0.00, null=True)
    
    def __str__(self):
       return str(self.id)

class Propietario(Cliente):
    direccion = models.CharField(max_length=50, null=True)

class Comprador(Cliente):
    zona = models.IntegerField(default=0)
    tipoPropiedad = models.CharField(max_length=20, default="casa")
    presupuesto = models.FloatField(default=0.0)

class Intermediario(Cliente):
    comision = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    experiencia = models.IntegerField(default=0)

class CamposAdicionales(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    tipo = models.CharField(max_length=35, default="string")
    tabla = models.IntegerField(default=0)

class ValoresAdicionales(models.Model):
    id_campo = models.ForeignKey(CamposAdicionales, on_delete=models.CASCADE)
    id_tupla = models.IntegerField(default=0)
    valor = models.CharField(max_length=35, default="")
    