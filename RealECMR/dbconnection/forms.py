from django import forms
from django.db import connection
from .models import CamposAdicionales, Propiedad

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
    # tabla = forms.CharField(max_length=50)

    def agregarCampo(self, tablaNum):
        data = self.cleaned_data
        id = CamposAdicionales.objects.count()
        # if data.get("tabla") == "propiedad":
        #     tablaNum = 0
        # elif data.get("tabla") == "propietario":
        #     tablaNum = 1
        cursor = connection.cursor()
        cursor.execute("INSERT INTO dbconnection_camposadicionales VALUES (%s, %s, %s, %s)", [id, data.get("nombre"), data.get("tipo"), tablaNum])


class AgregarPropiedad(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['direccion', 'valuacion', 'tipo', 'informacion', 'tamano']

    def agregarPropiedad(self):
        foto = None
        data = self.cleaned_data
        id = Propiedad.objects.count()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO dbconnection_propiedad VALUES (%s, %s, %s, %s, %s, %s, %s)", [id, data.get("direccion"), data.get("valuacion"), data.get("tipo"), data.get("informacion"), foto, data.get("tamano")])