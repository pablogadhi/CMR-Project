from django import forms
from django.db import connection
from .models import *
from .utilities import dictfetchall

class AgregarCampoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    TIPOCAMPO = (
        ('string', 'Texto'),
        ('int', 'Entero'),
        ('float', 'Real')
    )
    tipo = forms.ChoiceField(choices=TIPOCAMPO)
    # tabla = forms.CharField(max_length=50)

    def agregar(self, tablaNum):
        data = self.cleaned_data
        cursor = connection.cursor()
        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla=%s", ['camposadicionales'])
        id = dictfetchall(cursor)
        id = id[0]['cantidad']
        cursor.execute("INSERT INTO dbconnection_camposadicionales VALUES (%s, %s, %s, %s)",
                        [id, data.get("nombre"), data.get("tipo"), tablaNum])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [id+1, 'camposadicionales'])


class PropiedadForm(forms.Form):
    propietario = forms.IntegerField(widget=forms.TextInput)
    intermediario = forms.IntegerField(widget=forms.TextInput)
    direccion = forms.CharField(max_length=50)
    valuacion = forms.FloatField(widget=forms.TextInput)
    TIPOBIEN = (
        ('Apartamento', 'Apartamento'),
        ('Casa', 'Casa'),
        ('Terreno', 'Terreno'),
        ('Otro', 'Otro')
    )
    tipo = forms.ChoiceField(choices=TIPOBIEN)
    informacion = forms.CharField(max_length=500)
    foto = forms.FileField(required=False)
    tamano = forms.DecimalField(widget=forms.TextInput)


class CompradorForm(forms.Form):
    activo = forms.BooleanField(initial=True)
    nombre = forms.CharField(max_length=50)
    TIPOSEXO = (
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    )
    sexo = forms.ChoiceField(choices=TIPOSEXO)
    edad = forms.IntegerField(widget=forms.TextInput)
    telefono = forms.IntegerField(widget=forms.TextInput)
    mail = forms.EmailField()
    cuenta = forms.CharField()
    fechaInicio = forms.DateField(
        label='Fecha de Inicio', widget=forms.SelectDateWidget)
    TIPOREP = (
        ('Normal', 'Normal'),
        ('Buena', 'Buena'),
        ('Mala', 'Mala'),
    )
    reputacion = forms.ChoiceField(choices=TIPOREP)
    foto = forms.FileField(required=False)
    zona = forms.IntegerField()
    TIPOBIEN = (
        ('Apartamento', 'Apartamento'),
        ('Casa', 'Casa'),
        ('Terreno', 'Terreno'),
        ('Otro', 'Otro')
    )
    tipoPropiedad = forms.ChoiceField(
        choices=TIPOBIEN, label='Tipo de Propiedad')
    presupuesto = forms.FloatField(widget=forms.TextInput)


class PropietarioForm(forms.Form):
    activo = forms.BooleanField(initial=True, required=False)
    nombre = forms.CharField(max_length=50)
    TIPOSEXO = (
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    )
    sexo = forms.ChoiceField(choices=TIPOSEXO)
    edad = forms.IntegerField(widget=forms.TextInput)
    telefono = forms.IntegerField(widget=forms.TextInput)
    mail = forms.EmailField()
    cuenta = forms.CharField(required=False)
    fechaInicio = forms.DateField(
        label='Fecha de Inicio', widget=forms.SelectDateWidget)
    TIPOREP = (
        ('Normal', 'Normal'),
        ('Buena', 'Buena'),
        ('Mala', 'Mala'),
    )
    reputacion = forms.ChoiceField(choices=TIPOREP)
    foto = forms.FileField(required=False)
    direccion = forms.CharField(max_length=50)

    def agregar(self, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='propietario'")
        id = dictfetchall(cursor)
        id = id[0]['cantidad']
        activo = str(data.get("activo"))
        nombre = data.get("nombre")
        sexo = data.get("sexo")
        edad = data.get("edad")
        telefono = data.get("telefono")
        mail = data.get("mail")
        cuenta = None
        fechaInicio = data.get("fechaInicio")
        reputacion = 'Normal'
        foto = None
        direccion = data.get("direccion")

        cursor.execute("INSERT INTO dbconnection_propietario VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        [id, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, direccion])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [id+1, 'propietario'])

        for campo in camposAdicionales:
            id_extra = ValoresAdicionales.objects.count()
            id_campo = campo.get("id")
            id_tupla = id
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)",
                            [id_extra, id_tupla, valor, id_campo])

    def actualizar(self, idTupla, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()

        activo = str(data.get("activo"))
        nombre = data.get("nombre")
        sexo = data.get("sexo")
        edad = data.get("edad")
        telefono = data.get("telefono")
        mail = data.get("mail")
        cuenta = None
        fechaInicio = data.get("fechaInicio")
        reputacion = 'Normal'
        foto = None
        direccion = data.get("direccion")

        cursor.execute("UPDATE dbconnection_propietario SET id=%s, activo=%s, nombre=%s, sexo=%s, edad=%s, telefono=%s, mail=%s, cuenta=%s, fechainicio=%s, reputacion=%s, foto=%s, direccion=%s WHERE id=%s",
                        [idTupla, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, direccion, idTupla])

        for campo in camposAdicionales:
            id_campo = campo.get("id")
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("SELECT id FROM dbconnection_valoresadicionales WHERE id_tupla=%s AND campo_id=%s",
                            [idTupla, id_campo])
            vaId = dictfetchall(cursor)
            if vaId != []:
                cursor.execute("UPDATE dbconnection_valoresadicionales SET valor=%s WHERE id_tupla=%s AND campo_id=%s",
                            [valor, idTupla, id_campo])
            else:
                id_extra = ValoresAdicionales.objects.count()
                cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)",
                            [id_extra, idTupla, valor, id_campo])


    def eliminar(self, idTupla):
        cursor = connection.cursor()
        cursor.execute("DELETE FROM dbconnection_propietario WHERE id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_valoresadicionales WHERE id=%s", [idTupla])

            
class IntermediarioForm(forms.Form):
    activo = forms.BooleanField(initial=True)
    nombre = forms.CharField(max_length=50)
    TIPOSEXO = (
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    )
    sexo = forms.ChoiceField(choices=TIPOSEXO)
    edad = forms.IntegerField(widget=forms.TextInput)
    telefono = forms.IntegerField(widget=forms.TextInput)
    mail = forms.EmailField()
    cuenta = forms.CharField()
    fechaInicio = forms.DateField(
        label='Fecha de Inicio', widget=forms.SelectDateWidget)
    TIPOREP = (
        ('Normal', 'Normal'),
        ('Buena', 'Buena'),
        ('Mala', 'Mala'),
    )
    reputacion = forms.ChoiceField(choices=TIPOREP)
    foto = forms.FileField(required=False)
    comision = forms.DecimalField(widget=forms.TextInput)
    experiencia = forms.IntegerField(widget=forms.TextInput)

class FiltroCompradores(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
