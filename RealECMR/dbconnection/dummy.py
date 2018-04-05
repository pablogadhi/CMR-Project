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

class PropietarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Propietario
    id = factory.Sequence(lambda n: '%i' % n) 
    activo = True
    nombre = factory.Faker('name', 'es_MX')
    sexo = factory.LazyFunction(randomSex)
    edad = random.randint(18, 99)
    telefono = random.randint(10000000, 99999999)
    mail = factory.LazyAttribute(lambda obj: '%s@mail.com' % genUserName(obj.nombre))
    cuenta = None
    fechainicio = factory.Faker('date_this_decade')
    reputacion = factory.LazyFunction(randomReputacion)
    foto = None
    direccion = factory.Faker('address', 'es_MX')

def generateDummy():
    PropietarioFactory.create_batch(100)
