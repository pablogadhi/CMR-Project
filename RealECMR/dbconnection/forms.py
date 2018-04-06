from django import forms
from django.db import connection
from .models import *
from .utilities import dictfetchall
import base64


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
        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla=%s", [
                       'camposadicionales'])
        id = dictfetchall(cursor)
        id = id[0]['cantidad']
        cursor.execute("INSERT INTO dbconnection_camposadicionales VALUES (%s, %s, %s, %s)",
                        [id, data.get("nombre"), data.get("tipo"), tablaNum])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [
                       id+1, 'camposadicionales'])

class FilPropietarioForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    edad = forms.IntegerField(widget=forms.TextInput, required=False, initial='0')
    direccion = forms.CharField(max_length=50, required=False)

    def filtrar(self):
        data= self.cleaned_data
        nombre = data.get('nombre')
        edad = data.get('edad')
        direccion = data.get('direccion')
        return nombre,edad,direccion

class FilCompradorForm(forms.Form):
    TIPOREP = (
        ('',''),
        ('Buena','Buena'),
        ('Normal','Normal'),
        ('Mala','Mala'),
    )
    reputacion = forms.ChoiceField(choices=TIPOREP, required=False)
    presupuesto = forms.FloatField(widget=forms.TextInput, required=False, initial='0')
    TIPOBIEN = (
        ('',''),
        ('Apartamento','Apartamento'),
        ('Casa','Casa'),
        ('Terreno','Terreno'),
        ('Otro','Otro')
    )
    busca = forms.ChoiceField(choices=TIPOBIEN, required=False)

    def filtrar(self):
        data= self.cleaned_data
        nombre = data.get('reputacion')
        edad = data.get('presupuesto')
        direccion = data.get('busca')
        return nombre,edad,direccion

class FilIntermediariosForm(forms.Form):
    TIPOSEXO = (
        ('',''),
        ('Femenino','Femenino'),
        ('Masculino','Masculino'),
    )
    sexo = forms.ChoiceField(choices=TIPOSEXO, required=False)
    comision = forms.FloatField(widget=forms.TextInput, required=False, initial='0')
    experiencia = forms.IntegerField(required=False, initial='0')
    def filtrar(self):
        data= self.cleaned_data
        sexo = data.get('sexo')
        comision = data.get('comision')
        experiencia = data.get('experiencia')
        return sexo,comision,experiencia

class FilPropiedadForm(forms.Form):
    direccion = forms.CharField(max_length=50, required=False)
    valuacion = forms.FloatField(widget=forms.TextInput, required=False, initial='0')
    TIPOBIEN = (
        ('',''),
        ('Apartamento','Apartamento'),
        ('Casa','Casa'),
        ('Terreno','Terreno'),
        ('Otro','Otro')
    )
    tipo = forms.ChoiceField(choices=TIPOBIEN, required=False)

    def filtrar(self):
        data= self.cleaned_data
        direccion = data.get('direccion')
        valuacion = data.get('valuacion')
        tipo = data.get('tipo')
        return direccion,valuacion,tipo

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['propietario', 'intermediario', 'direccion', 'valuacion', 'tipo', 'informacion', 'foto', 'tamano']
        widgets = {
                'valuacion': forms.TextInput(),
                'foto': forms.FileInput(attrs={'required': False}),
                'tamano': forms.TextInput()
                }
        labels = {
            'tamano': 'Tamaño (metros cuatrados)',
            'valuacion': 'Valuacion (Q)'
        }
        

    def agregar(self, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='propiedad'")
        id = dictfetchall(cursor)
        id = id[0]['cantidad']
        propietario = data.get('propietario')
        propietario = propietario.id
        intermediario = data.get('intermediario')
        intermediario = intermediario.id
        direccion = data.get('direccion')
        valuacion = data.get('valuacion')
        tipo = data.get('tipo')
        informacion = data.get('informacion')
        foto = None
        tamano = data.get('tamano')

        cursor.execute("INSERT INTO dbconnection_propiedad VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        [id, direccion, valuacion, tipo, informacion, foto, tamano, intermediario, propietario])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [id+1, 'propiedad'])

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='valoresadicionales'")
        cantidadCA = dictfetchall(cursor)
        cantidadCA = cantidadCA[0]['cantidad']
        for campo in camposAdicionales:
            id_extra = cantidadCA
            id_campo = campo.get("id")
            id_tupla = id
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)",
                            [id_extra, id_tupla, valor, id_campo])
            cantidadCA += 1
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [cantidadCA, 'valoresadicionales'])

    def actualizar(self, idTupla, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()

        propietario = data.get('propietario')
        propietario = propietario.id
        intermediario = data.get('intermediario')
        intermediario = intermediario.id
        direccion = data.get('direccion')
        valuacion = data.get('valuacion')
        tipo = data.get('tipo')
        informacion = data.get('informacion')
        foto = None
        tamano = data.get('tamano')

        cursor.execute("UPDATE dbconnection_propiedad SET id=%s, propietario_id=%s, intermediario_id=%s, direccion=%s, valuacion=%s, tipo=%s, informacion=%s, foto=%s, tamano=%s WHERE id=%s",
                        [idTupla, propietario, intermediario, direccion, valuacion, tipo, informacion, foto, tamano, idTupla])

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
        cursor.execute("DELETE FROM dbconnection_visita WHERE propiedad_id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_administra WHERE propiedad_id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_propiedad WHERE id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_valoresadicionales WHERE id=%s", [idTupla])

class CompradorForm(forms.ModelForm):
    class Meta:
        model = Comprador
        fields = ['activo', 'nombre', 'sexo', 'edad', 'telefono', 'mail', 'cuenta',
            'fechainicio', 'reputacion', 'foto', 'zona', 'tipopropiedad', 'presupuesto']
        widgets = {
                'activo': forms.CheckboxInput(attrs={'initial': True, 'required': False}),
                'edad': forms.TextInput(),
                'telefono': forms.TextInput(),
                'fechainicio': forms.SelectDateWidget(),
                'foto': forms.FileInput(attrs={'required': False}),
                'zona': forms.TextInput(),
                'presupuesto': forms.TextInput()
                }
        labels = {
                'fechainicio': 'Fecha de Inicio',
                'tipopropiedad': 'Tipo de Propiedad',
                'presupuesto': 'Presupuesto (Q)'
                }

    def agregar(self, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='comprador'")
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
        zona = data.get("zona")
        tipopropiedad = data.get('tipopropiedad')
        presupuesto = data.get('presupuesto')

        cursor.execute("INSERT INTO dbconnection_comprador VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        [id, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, zona, tipopropiedad, presupuesto])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [id+1, 'comprador'])

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='valoresadicionales'")
        cantidadCA = dictfetchall(cursor)
        cantidadCA = cantidadCA[0]['cantidad']
        for campo in camposAdicionales:
            id_extra = cantidadCA
            id_campo = campo.get("id")
            id_tupla = id
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)",
                            [id_extra, id_tupla, valor, id_campo])
            cantidadCA += 1
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [cantidadCA, 'valoresadicionales'])

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
        zona = data.get("zona")
        tipopropiedad = data.get('tipopropiedad')
        presupuesto = data.get('presupuesto')

        cursor.execute("UPDATE dbconnection_comprador SET id=%s, activo=%s, nombre=%s, sexo=%s, edad=%s, telefono=%s, mail=%s, cuenta=%s, fechainicio=%s, reputacion=%s, foto=%s, zona=%s, tipopropiedad=%s, presupuesto=%s WHERE id=%s",
                        [idTupla, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, zona, tipopropiedad, presupuesto, idTupla])

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
        cursor.execute("DELETE FROM dbconnection_visita WHERE comprador_id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_comprador WHERE id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_valoresadicionales WHERE id=%s", [idTupla])

class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = ['activo', 'nombre', 'sexo', 'edad', 'telefono', 'mail', 'cuenta', 'fechainicio', 'reputacion', 'foto', 'direccion']
        widgets = {
                'activo': forms.CheckboxInput(attrs={'initial':True, 'required':False}),
                'edad': forms.TextInput(),
                'telefono': forms.TextInput(),
                'fechainicio': forms.SelectDateWidget(),
                'foto': forms.FileInput(attrs={'required':False}),
                }
        labels = {
                'fechainicio': 'Fecha de Inicio'
                }

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
        fechaInicio = data.get("fechainicio")
        reputacion = data.get('reputacion')
        foto = data.get("foto")
        direccion = data.get("direccion")

        cursor.execute("INSERT INTO dbconnection_propietario VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        [id, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, direccion])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [id+1, 'propietario'])

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='valoresadicionales'")
        cantidadCA = dictfetchall(cursor)
        cantidadCA = cantidadCA[0]['cantidad']
        for campo in camposAdicionales:
            id_extra = cantidadCA
            id_campo = campo.get("id")
            id_tupla = id
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)",
                            [id_extra, id_tupla, valor, id_campo])
            cantidadCA += 1
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [cantidadCA, 'valoresadicionales'])

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
        fechaInicio = data.get("fechainicio")
        reputacion = 'Normal'
        foto = (data.get('foto'))
        foto = str((foto.file).getvalue())
        # foto = str(base64.b64encode(foto))
        # print(foto)
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
        cursor.execute("SELECT id FROM dbconnection_propiedad WHERE propietario_id=%s", [idTupla])
        idPropiedad = dictfetchall(cursor)
        idPropiedad = idPropiedad[0]['id']
        cursor.execute("DELETE FROM dbconnection_visita WHERE propiedad_id=%s", [idPropiedad])
        cursor.execute("DELETE FROM dbconnection_administra WHERE propietario_id=%s OR propiedad_id=%s", [idTupla, idPropiedad])
        cursor.execute("DELETE FROM dbconnection_propiedad WHERE propietario_id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_propietario WHERE id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_valoresadicionales WHERE id=%s", [idTupla])

            
class IntermediarioForm(forms.ModelForm):
    class Meta:
        model = Intermediario
        fields = ['activo', 'nombre', 'sexo', 'edad', 'telefono', 'mail', 'cuenta', 'fechainicio', 'reputacion', 'foto', 'comision', 'experiencia']
        widgets = {
                'activo': forms.CheckboxInput(attrs={'initial':True, 'required':False}),
                'edad': forms.TextInput(),
                'telefono': forms.TextInput(),
                'fechainicio': forms.SelectDateWidget(),
                'foto': forms.FileInput(attrs={'required':False}),
                'comision': forms.TextInput(),
                }
        labels = {
                'fechainicio': 'Fecha de Inicio',
                'comision': 'Comision (Q)',
                'experiencia': 'Experiencia (Años)'
                }

    def agregar(self, camposAdicionales, valoresAdicionales):
        data = self.cleaned_data
        cursor = connection.cursor()

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='intermediario'")
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
        comision = str(data.get("comision"))
        experiencia = str(data.get("experiencia"))

        cursor.execute("INSERT INTO dbconnection_intermediario VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        [id, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, comision, experiencia])
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [id+1, 'intermediario'])

        cursor.execute("SELECT cantidad FROM dbconnection_cantidadtuplas WHERE nombre_tabla='valoresadicionales'")
        cantidadCA = dictfetchall(cursor)
        cantidadCA = cantidadCA[0]['cantidad']
        for campo in camposAdicionales:
            id_extra = cantidadCA
            id_campo = campo.get("id")
            id_tupla = id
            campoKey = "ca" + str(id_campo)
            valor = valoresAdicionales.get(campoKey)
            cursor.execute("INSERT INTO dbconnection_valoresadicionales VALUES (%s, %s, %s, %s)",
                            [id_extra, id_tupla, valor, id_campo])
            cantidadCA += 1
        cursor.execute("UPDATE dbconnection_cantidadtuplas SET cantidad=%s WHERE nombre_tabla=%s", [cantidadCA, 'valoresadicionales'])

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
        comision = data.get("comision")
        experiencia = data.get("experiencia")

        cursor.execute("UPDATE dbconnection_intermediario SET id=%s, activo=%s, nombre=%s, sexo=%s, edad=%s, telefono=%s, mail=%s, cuenta=%s, fechainicio=%s, reputacion=%s, foto=%s, comision=%s, experiencia=%s WHERE id=%s",
                        [idTupla, activo, nombre, sexo, edad, telefono, mail, cuenta, fechaInicio, reputacion, foto, comision, experiencia, idTupla])

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
        cursor.execute("SELECT id FROM dbconnection_propiedad WHERE propietario_id=%s", [idTupla])
        idPropiedad = dictfetchall(cursor)
        idPropiedad = idPropiedad[0]['id']
        cursor.execute("DELETE FROM dbconnection_visita WHERE propiedad_id=%s", [idPropiedad])
        cursor.execute("DELETE FROM dbconnection_administra WHERE propiedad_id=%s", [idPropiedad])
        cursor.execute("DELETE FROM dbconnection_propiedad WHERE intermediario_id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_intermediario WHERE id=%s", [idTupla])
        cursor.execute("DELETE FROM dbconnection_valoresadicionales WHERE id=%s", [idTupla])

class FiltroCompradores(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
