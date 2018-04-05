from .models import *
import random
from django.db import models
import factory

def randomSex():
    sexos = ['Femenino', 'Masculino']
    return random.choice(sexos)

def genUserName(string):
    uname = string.replace(" ", "")
    return uname.lower()

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
    presupuesto = factory.Faker('pyfloat')

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

def generateDummy():
    PropietarioFactory.create_batch(100)
    CompradorFactory.create_batch(100)
    IntermediarioFactory.create_batch(100)
