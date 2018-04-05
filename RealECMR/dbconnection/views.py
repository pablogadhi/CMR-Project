from django.http import HttpResponse
from django.template import loader
from .forms import *
from django.shortcuts import render, get_object_or_404
from .models import *
from django.views import generic
from .dummy import generateDummy
from django.urls import reverse
from django.db import connection
from django.forms import formset_factory, BaseFormSet
from .utilities import dictfetchall

ele_propietario= ['%%',0,'%%']

def index(request):
    num_propietarios = Propietario.objects.all().count()
    num_compradores = Comprador.objects.all().count()
    num_propiedades = Propiedad.objects.all().count()
    num_intermediarios = Intermediario.objects.all().count()
    num_visitas = Visita.objects.all().count()
    num_tweets = Tweet.objects.all().count()
    return render(
        request,
        'index.html',
        context={'num_propietarios': num_propietarios, 'num_compradores': num_compradores,
                 'num_propiedades': num_propiedades, 'num_intermediarios': num_intermediarios,
                 'num_visitas': num_visitas,'num_tweets': num_tweets },
    )


def dummy(request):
    generateDummy()
    return HttpResponse("Dummy Generado!")


class PropetarioListView(generic.edit.FormMixin, generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    # model = Propietario
    cursor = connection.cursor()
    campos_adicionales = []
    UpdateFormset = formset_factory(PropietarioForm)

    context_object_name = 'propietario_list'
    template_name = 'dbconnection/propietario_list.html'
    paginate_by = 100
    form_class = AgregarCampoForm
    second_form_class = PropietarioForm
    third_form_class = FilPropietarioForm
   
    def get_success_url(self):
        return reverse('propietarios')

    def get_context_data(self, **kwargs):
        #self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['campos_adicionales'] = self.campos_adicionales
        context['form'] = self.get_form()
        context['second_form'] = self.get_form(self.get_second_form_class())
        context['third_form'] = self.get_form(self.get_third_form_class())
        context['update_formset'] = self.UpdateFormset
        context['uform_index'] = 0
        return context

    def post(self, request, *args, **kwargs):
        if 'addCampo' in request.POST:
            form = self.get_form(self.get_form_class())
            if form.is_valid():
                form.agregar(1)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'addFila' in request.POST:
            form = self.get_form(self.get_second_form_class())
            if form.is_valid():
                self.cursor.execute(
                    "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 1")
                valoresA = {}
                campos_adicionales = dictfetchall(self.cursor)
                for i in campos_adicionales:
                    key = "ca"+str(i['id'])
                    valoresA[key] = request.POST.get(key)
                form.agregar(campos_adicionales, valoresA)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'updateFila' in request.POST:
            data = request.POST.copy()
            self.cursor.execute("SELECT COUNT(*) FROM dbconnection_propietario")
            size = dictfetchall(self.cursor)
            self.cursor.execute("SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 1")
            camposA = dictfetchall(self.cursor)
            valoresA = {}
            for c in camposA:
                key = "ca" + str(c['id'])
                valoresA[key] = data.get(key) 
            data.update({'form-TOTAL_FORMS': size[0]['count'],
                        'form-INITIAL_FORMS': size[0]['count'],
                        'form-MAX_NUM_FORMS': ''})
            formset = self.UpdateFormset(data)
            count = 0
            form = None
            for f in formset:
                if f.is_valid():
                    f.actualizar(count, camposA, valoresA)
                    return self.form_valid(form)
                else:
                    print(count)
                    print(f.errors)
                count += 1
            return self.form_invalid(form)
        elif 'deleteFila' in request.POST:
            data = request.POST.copy()
            self.cursor.execute("SELECT COUNT(*) FROM dbconnection_propietario")
            size = dictfetchall(self.cursor)
            data.update({'form-TOTAL_FORMS': size[0]['count'],
                        'form-INITIAL_FORMS': size[0]['count'],
                        'form-MAX_NUM_FORMS': ''})
            formset = self.UpdateFormset(data)
            count = 0
            form = None
            for f in formset:
                if f.is_valid():
                    f.eliminar(count)
                    return self.form_valid(form)
                else:
                    print(count)
                    print(f.errors)
                count += 1
            return self.form_invalid(form)
        if 'filtrar' in request.POST:
            form = self.get_form(self.get_third_form_class())
            if form.is_valid():
                elementos=form.filtrar()
                global ele_propietario
                ele_propietario[0]=elementos[0]
                ele_propietario[1]=elementos[1]
                ele_propietario[2]=elementos[2]
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid Form!")
        return super().form_invalid(form)

    def get_second_form_class(self):
        return self.second_form_class

    def get_third_form_class(self):
        return self.third_form_class

    def get_queryset(self):
        self.cursor.execute(
        	"SELECT * FROM dbconnection_propietario WHERE nombre LIKE %s AND edad > %s AND direccion LIKE %s ORDER BY id",['%'+ele_propietario[0]+'%',ele_propietario[1],'%'+ele_propietario[2]+'%'])
        print(chr(39)+'%'+'e'+'%'+chr(39))
        tabla = dictfetchall(self.cursor)
        self.cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 1")
        self.campos_adicionales = dictfetchall(self.cursor)
        for prop in tabla:
            self.cursor.execute(
                "SELECT * FROM dbconnection_valoresadicionales as va WHERE va.id_tupla = %s", [prop["id"]])
            result = dictfetchall(self.cursor)
            for i in range(len(self.campos_adicionales)):
                try:
                    prop['ca'+str(self.campos_adicionales[i]['id'])
                         ] = result[i]["valor"]
                except:
                    prop['ca'+str(self.campos_adicionales[i]['id'])] = None

        AgregarFormSet = formset_factory(PropietarioForm, extra=len(tabla))
        self.UpdateFormset = AgregarFormSet(initial=tabla)
        return tabla


class VisitaListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    #model = Visita

    cursor = connection.cursor()

    context_object_name = 'visita_list'
    template_name = 'dbconnection/visita_list.html'
    paginate_by = 100

    def get_success_url(self):
        return reverse('visitas')

    def get_context_data(self, **kwargs):
        #self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['prueba'] = 3
        return context

    def get_queryset(self):
        self.cursor.execute(
        	"SELECT v.id,v.fecha,c.nombre FROM dbconnection_visita as v, dbconnection_comprador as c, dbconnection_propietario as p, dbconnection_intermediario as i  WHERE v.comprador_id=c.id or v.comprador_id=p.id or v.comprador_id=i.id")
        tabla = dictfetchall(self.cursor)
        return tabla


class AdministraListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    model = Administra
    paginate_by = 100


class TweetListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    model = Tweet
    paginate_by = 100




class IntermediarioListView(generic.edit.FormMixin, generic.ListView):
    """
    Generic class-based view for a list of Intermediario.
    """
    model = Intermediario
    paginate_by = 10
    form_class = AgregarCampoForm

    def get_success_url(self):
        return reverse('intermediarios')

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 3")
        context = super().get_context_data(**kwargs)
        context['campos_adicionales'] = dictfetchall(cursor)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.agregar(3)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    


class CompradorListView(generic.edit.FormMixin, generic.ListView):
    """
    Generic class-based view for a list of Comprador.
    """
    model = Comprador
    paginate_by = 10
    form_class = AgregarCampoForm
    second_form_class = CompradorForm

    def get_success_url(self):
        return reverse('propiedades')

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        cursor = connection.cursor()
        context = super().get_context_data(**kwargs)
        cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 2")
        context['campos_adicionales'] = dictfetchall(cursor)
        context['form'] = self.get_form()
        context['second_form'] = self.get_form(self.get_second_form_class())
        return context

    def post(self, request, *args, **kwargs):
        if 'addCampo' in request.POST:
            form = self.get_form(self.get_form_class())
            if form.is_valid():
                form.agregar(2)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'addFila' in request.POST:
            form = self.get_form(self.get_second_form_class())
            if form.is_valid():
                form.agregar()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid Form!")
        return super().form_invalid(form)

    def get_second_form_class(self):
        return self.second_form_class


class PropiedadListView(generic.edit.FormMixin, generic.ListView):
    """
    Generic class-based view for a list of Propiedad.
    """
    model = Propiedad
    paginate_by = 10
    form_class = AgregarCampoForm
    second_form_class = PropiedadForm

    def get_success_url(self):
        return reverse('propiedades')

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        context = super().get_context_data(**kwargs)
        cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 0")
        context['campos_adicionales'] = dictfetchall(cursor)
        context['form'] = self.get_form()
        context['second_form'] = self.get_form(self.get_second_form_class())
        return context

    def post(self, request, *args, **kwargs):
        if 'addCampo' in request.POST:
            form = self.get_form(self.get_form_class())
            if form.is_valid():
                form.agregar(0)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'addFila' in request.POST:
            form = self.get_form(self.get_second_form_class())
            if form.is_valid():
                form.agregar()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_second_form_class(self):
        return self.second_form_class


class PropiedadDetailView(generic.ListView):
    """
    Generic class-based detail for a list of Propiedad.
    """
    model = Propiedad

