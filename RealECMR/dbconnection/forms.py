from django import forms
from django.db import connection
from .models import *


class AgregarCampoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    TIPOCAMPO = (
        ('string', 'Texto'),
        ('int', 'Entero'),
        ('float', 'Real')
    )
    tipo = forms.ChoiceField(choices=TIPOCAMPO)
    # tabla = forms.CharField(max_length=50)

    def agregarCampo(self, tablaNum):
        data = self.cleaned_data
        id = CamposAdicionales.objects.count()
        # if data.get("tabla") == "propiedad":
        #     tablaNum = 0
        # elif data.get("tabla") == "propietario":
        #     tablaNum = 1
        cursor = connection.cursor()
        cursor.execute("INSERT INTO dbconnection_camposadicionales VALUES (%s, %s, %s, %s)", [
                       id, data.get("nombre"), data.get("tipo"), tablaNum])


class AgregarPropiedad(forms.Form):
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

    def agregarPropiedad(self):
        foto = None
        data = self.cleaned_data
        id = Propiedad.objects.count()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO dbconnection_propiedad VALUES (%s, %s, %s, %s, %s, %s, %s)", [id, data.get(
            "direccion"), data.get("valuacion"), data.get("tipo"), data.get("informacion"), foto, data.get("tamano")])


class AgregarComprador(forms.Form):
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


class AgregarPropietario(forms.Form):
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
    direccion = forms.CharField(max_length=50)

    def agregarPropietario(self, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()
        id = Propietario.objects.count()
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
        cursor.execute("INSERT INTO dbconnection_propietario VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [
                       id, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, direccion])
        for campo in camposAdicionales:
            id_extra = ValoresAdicionales.objects.count()
            id_campo = campo.get("id")
            id_tupla = id
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)", [
                           id_extra, id_tupla, valor, id_campo])


class AgregarIntermediario(forms.Form):
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
