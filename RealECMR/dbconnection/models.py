from django.db import models
from django.urls import reverse

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    edad = models.IntegerField(default=0)
    telefono = models.IntegerField(default=0)
    sexo = models.CharField(max_length=10, default="femenino")
    rol = models.CharField(max_length=15, default="comprador")
    foto = models.ImageField(null=True)
    fechaInicio = models.DateField(null=True)
    activo = models.BooleanField(default=True)
    mail = models.EmailField(null=True)
    
    def __str__(self):
       return self.nombre

    def get_absolute_url(self):
        return reverse('detalle-cliente',args=[str(self.id)])
    
    class Meta:
        abstract = True

class Propiedad(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=50, null=True)
    valuacion = models.FloatField(default=0.0)
    tipo = models.CharField(max_length=20, default="casa")
    informacion = models.CharField(max_length=500, null=True)
    foto = models.ImageField(null=True)
    tamano = models.DecimalField(decimal_places=2, max_digits=8, default=0.00, null=True)
    
    def __str__(self):
       return str(self.id)

class Propietario(Cliente):
    bienPoseido = models.ForeignKey(Propiedad, on_delete=models.CASCADE, default=0)
    direccion = models.CharField(max_length=50, null=True)

class Comprador(Cliente):
    zona = models.IntegerField(default=0)
    tipoPropiedad = models.CharField(max_length=20, default="casa")
    presupuesto = models.FloatField(default=0.0)

class Intermediario(models.Model):
    id = models.AutoField(primary_key=True)
    comision = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    experiencia = models.IntegerField(default=0)
    nombre = models.CharField(max_length=35, null=True)
    
    def __str__(self):
       return self.nombre

class CamposAdicionales(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    tipo = models.CharField(max_length=35, default="string")
    tabla = models.IntegerField(default=0)

class ValoresAdicionales(models.Model):
    id_campo = models.ForeignKey(CamposAdicionales, on_delete=models.CASCADE)
    id_tupla = models.IntegerField(default=0)
    valor = models.CharField(max_length=35, default="")
    