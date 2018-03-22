from .models import *
import random
from django.db import models


def generateDummy():

    Propiedad.objects.all().delete() 
    Propietario.objects.all().delete() 
    Comprador.objects.all().delete() 
    Intermediario.objects.all().delete() 

    nombres = ['Carlos', 'Juan', 'Maria', 'Pedro', 'Gonzalo',
               'Luisa', 'Sofia', 'Fernanda', 'Migue', 'Gabriela']
    apellidos = ['Rodriguez', 'Sanchez', 'Gutierrez', 'Lopez',
                 'Fernandez', 'Juarez', 'Perez', 'Maldonado', 'Ramos']
    sexos = ['femenino', 'masculino', 'otro']
    estado = [True, False]
    domains = ['@gmail.com', '@hotmail.com', '@yahoo.com']
    tipos = ['casa', 'apartamento', 'oficina', 'bodega', 'terreno']

    propiedades = []

    for i in range(100):
        propiedad = Propiedad(direccion="direccion",
                              valuacion=random.uniform(0, 80000),
                              tipo=random.choice(tipos),
                              tamano=random.uniform(100, 100000)
                              )
        propiedad.save()
        propiedades.append(propiedad.id)

    for i in range(100):
        nombreE = random.choice(nombres)
        apellidoE = random.choice(apellidos)
        propietario = Propietario(nombre=nombreE + " " + apellidoE,
                                  edad=random.randint(20, 80),
                                  telefono=random.randint(10000000, 99999999),
                                  sexo=random.choice(sexos),
                                  rol="propietario",
                                  activo=random.choice(estado),
                                  mail=nombreE.lower()+apellidoE.lower()+random.choice(domains),
                                  )

        propietario.bienPoseido_id=random.choice(propiedades)
        propietario.save()

    for i in range(100):
        nombreE = random.choice(nombres)
        apellidoE = random.choice(apellidos)
        comprador = Comprador(nombre=nombreE + " " + apellidoE,
                              edad=random.randint(20, 80),
                              telefono=random.randint(10000000, 99999999),
                              sexo=random.choice(sexos),
                              rol="comprador",
                              activo=random.choice(estado),
                              mail=nombreE.lower()+apellidoE.lower()+random.choice(domains),
                              zona=random.randint(1, 25),
                              tipoPropiedad=random.choice(tipos),
                              presupuesto=random.uniform(0, 8000)
                              )
        comprador.save()

    for i in range(100):
        nombreE = random.choice(nombres)
        apellidoE = random.choice(apellidos)
        inter = Intermediario(nombre=nombreE + " " + apellidoE,
                              comision=random.random(),
                              experiencia=random.randint(0, 40)

                              )
        inter.save()
