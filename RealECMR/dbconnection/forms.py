from django import forms
from django.db import connection
from .models import CamposAdicionales

class QueryForm(forms.Form):
    query = forms.CharField(label='Query:', max_length=500,widget=forms.TextInput(attrs={'size':'120'}))

    def send(self):
        data = self.cleaned_data
        cursor = connection.cursor()
        cursor.execute(data.get("query"))
        return cursor.fetchall()
        # print(data.get("query"))

class AgregarCampoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    tipo = forms.CharField(max_length=35)
    tabla = forms.CharField(max_length=50)

    def agregarCampo(self):
        data = self.cleaned_data
        id = CamposAdicionales.objects.count()
        if data.get("tabla") == "propiedad":
            tablaNum = 0
        elif data.get("tabla") == "propietario":
            tablaNum = 1
        cursor = connection.cursor()
        cursor.execute("INSERT INTO dbconnection_camposadicionales VALUES (%s, %s, %s, %s)", [id, data.get("nombre"), data.get("tipo"), tablaNum])


