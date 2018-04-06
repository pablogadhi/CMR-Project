from .models import *
import random
from django.db import models
import factory
from django.db import connection
from .utilities import resetAllTables

def randomSex():
    sexos = ['Femenino', 'Masculino']
    return random.choice(sexos)

def genUserName(string):
    uname = string.replace(" ", "")
    uname = uname.lower()
    uname = uname.replace("á", "a")
    uname = uname.replace("é", "e")
    uname = uname.replace("í", "i")
    uname = uname.replace("ó", "o")
    uname = uname.replace("ú", "ú")
    uname = uname.replace("ñ", "n")
    uname = uname.replace("(", "")
    uname = uname.replace(")", "")
    return uname

def randomReputacion():
    reputaciones = ['Buena', 'Normal', 'Mala']
    return random.choice(reputaciones)

def randomAge():
    return random.randint(18, 99)

def randomPhone():
    return random.randint(10000000, 99999999)

def randomZona():
    return random.randint(1, 25)

def randomTipoBien():
    tipos = ['Apartamento', 'Casa', 'Terreno', 'Otro']
    return random.choice(tipos)

def randomPercentage():
    return random.uniform(0.00, 100.00)

def randomExp():
    return random.randint(0, 60)

def randomPresupuesto():
    return random.uniform(0.00, 999999.99)

def randomSize():
    return random.uniform(1000.00, 9999.99)

class PropietarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Propietario
    id = factory.Sequence(lambda n: '%i' % n) 
    activo = True
    nombre = factory.Faker('name', 'es_MX')
    sexo = factory.LazyFunction(randomSex)
    edad = factory.LazyFunction(randomAge)
    telefono = factory.LazyFunction(randomPhone)
    mail = factory.LazyAttribute(lambda obj: '%s@mail.com' % genUserName(obj.nombre))
    cuenta = None
    fechainicio = factory.Faker('date_this_decade')
    reputacion = factory.LazyFunction(randomReputacion)
    foto = None
    direccion = factory.Faker('address', 'es_MX')

class CompradorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comprador
    id = factory.Sequence(lambda n: '%i' % n) 
    activo = True
    nombre = factory.Faker('name', 'es_MX')
    sexo = factory.LazyFunction(randomSex)
    edad = factory.LazyFunction(randomAge)
    telefono = factory.LazyFunction(randomPhone)
    mail = factory.LazyAttribute(lambda obj: '%s@mail.com' % genUserName(obj.nombre))
    cuenta = None
    fechainicio = factory.Faker('date_this_decade')
    reputacion = factory.LazyFunction(randomReputacion)
    foto = None
    zona = factory.LazyFunction(randomZona)
    tipopropiedad = factory.LazyFunction(randomTipoBien)
    presupuesto = factory.LazyFunction(randomPresupuesto)

class IntermediarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Intermediario

    id = factory.Sequence(lambda n: '%i' % n) 
    activo = True
    nombre = factory.Faker('name', 'es_MX')
    sexo = factory.LazyFunction(randomSex)
    edad = factory.LazyFunction(randomAge)
    telefono = factory.LazyFunction(randomPhone)
    mail = factory.LazyAttribute(lambda obj: '%s@mail.com' % genUserName(obj.nombre))
    cuenta = None
    fechainicio = factory.Faker('date_this_decade')
    reputacion = factory.LazyFunction(randomReputacion)
    foto = None
    comision = factory.LazyFunction(randomPercentage)
    experiencia = factory.LazyFunction(randomExp)

class PropiedadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Propiedad
    id = factory.Sequence(lambda n: '%i' % n) 
    propietario = factory.Iterator(Propietario.objects.all())
    intermediario = factory.Iterator(Intermediario.objects.all())
    direccion = factory.Faker('address', 'es_MX')
    valuacion = factory.LazyFunction(randomPresupuesto)
    tipo = factory.LazyFunction(randomTipoBien)
    informacion = factory.Faker('paragraph', 'es_MX')
    foto = None
    tamano = factory.LazyFunction(randomSize)

class VisitaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Visita
    id = factory.Sequence(lambda n: '%i' % n) 
    comprador = factory.Iterator(Comprador.objects.all())
    propiedad = factory.Iterator(Propiedad.objects.all())
    fecha = factory.Faker('date_this_decade')

class AdministraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administra
    propietario = factory.Iterator(Propietario.objects.all())
    propiedad = factory.Iterator(Propiedad.objects.all())
    fecha = factory.Faker('date_this_decade')

def generateDummy():
    cursor = connection.cursor()
    resetAllTables(cursor)
    PropietarioFactory.create_batch(40)
    CompradorFactory.create_batch(40)
    IntermediarioFactory.create_batch(40)
    PropiedadFactory.create_batch(40)
    VisitaFactory.create_batch(40)
    AdministraFactory.create_batch(40)
    cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=40 WHERE nombre_tabla='propietario'")
    cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=40 WHERE nombre_tabla='comprador'")
    cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=40 WHERE nombre_tabla='intermediario'")
    cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=40 WHERE nombre_tabla='propiedad'")
    cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=40 WHERE nombre_tabla='visita'")
    cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=40 WHERE nombre_tabla='administra'")
    
