from django.db import models

class Cliente(models.Model):
    id = models.AutoField()
    nombre = models.CharField(max_length=35)
    edad = models.IntegerField(default=0)
    telefono = models.IntegerField(default=0)
    sexo = models.CharField(max_length=10)
    rol = models.CharField(max_length=15)
    foto = models.ImageField()
    fechaInicio = models.DateField()
    activo = models.BooleanField()
    mail = models.EmailField()

class Propietario(models.Model):
    idP = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombreP = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    bienPoseido = models.CharField(max_length=20)
    direccion = models.CharField(max_length=50)

class Comprador(models.Model):
    idC = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombreC = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    zona = models.IntegerField(default=0)
    tipoPropiedad = models.CharField(max_length=20)
    presupuesto = models.FloatField()

class Propiedad(models.Model):
    direccion = models.CharField(max_length=50)
    valuacion = models.FloatField()
    tipo = models.CharField(max_length=20)
    informacion = models.CharField(max_length=100)
    fotos = models.ImageField()
    tamano = models.DecimalField(decimal_places=5, max_digits=3)

class Intermediario(models.Model):
    idI = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    comision = models.DecimalField(decimal_places=6, max_digits=2)
    experiencia = models.IntegerField(default=0)
    nombreI = models.CharField(max_length=35)
    
#    def __str__(self):
#        return self.name
# Create your models here.
