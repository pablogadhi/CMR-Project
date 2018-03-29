from django.http import HttpResponse
from django.template import loader
from .forms import *
from django.shortcuts import render, get_object_or_404
from .models import Cliente, Propietario, Comprador, Propiedad, Intermediario, CamposAdicionales, Visita, Administra
from django.views import generic
from .dummy import generateDummy
from django.urls import reverse
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def index(request):
    num_propietarios = Propietario.objects.all().count()
    num_compradores = Comprador.objects.all().count()
    num_propiedades = Propiedad.objects.all().count()
    num_intermediarios = Intermediario.objects.all().count()
    return render(
        request,
        'index.html',
        context={'num_propietarios': num_propietarios, 'num_compradores': num_compradores,
                 'num_propiedades': num_propiedades, 'num_intermediarios': num_intermediarios},
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
    context_object_name = 'propietario_list'
    template_name = 'dbconnection/propietario_list.html'
    paginate_by = 100
    form_class = AgregarCampoForm
    second_form_class = AgregarPropietario

    def get_success_url(self):
        return reverse('propietarios')

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['campos_adicionales'] = self.campos_adicionales
        context['form'] = self.get_form()
        context['second_form'] = self.get_form(self.get_second_form_class())
        return context

    def post(self, request, *args, **kwargs):
        if 'addCampo' in request.POST:
            form = self.get_form(self.get_form_class())
            if form.is_valid():
                form.agregarCampo(1)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'addFila' in request.POST:
            form = self.get_form(self.get_second_form_class())
            if form.is_valid():
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 1")
                valoresA = {}
                campos_adicionales = dictfetchall(cursor)
                for i in campos_adicionales:
                    key = "ca"+str(i['id'])
                    valoresA[key] = request.POST.get(key)
                form.agregarPropietario(campos_adicionales, valoresA)
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

    def get_queryset(self):
        self.cursor.execute("SELECT * FROM dbconnection_propietario")
        tabla = dictfetchall(self.cursor)
        self.cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 1")
        self.campos_adicionales = dictfetchall(self.cursor)
        for prop in tabla:
            self.cursor.execute("SELECT * FROM dbconnection_valoresadicionales as va WHERE va.id_tupla = %s", [prop["id"]])
            result = dictfetchall(self.cursor)
            for i in range(len(self.campos_adicionales)):
                try:
                    prop[str(self.campos_adicionales[i]['id'])] = result[i]["valor"]
                except:
                    prop[str(self.campos_adicionales[i]['id'])] = None
        
        return tabla


class VisitaListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    model = Visita
    paginate_by = 100


class AdministraListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    model = Administra
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
            form.agregarCampo(3)
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
    second_form_class = AgregarComprador

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
                form.agregarCampo(2)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'addFila' in request.POST:
            form = self.get_form(self.get_second_form_class())
            if form.is_valid():
                form.agregarPropiedad()
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
    second_form_class = AgregarPropiedad

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
                form.agregarCampo(0)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'addFila' in request.POST:
            form = self.get_form(self.get_second_form_class())
            if form.is_valid():
                form.agregarPropiedad()
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


class AgregarCampoView(generic.FormView):
    # model = CamposAdicionales
    # fields = ['nombre', 'tipo', 'tabla']
    form_class = AgregarCampoForm
    template_name = 'dbconnection/camposadicionales_form.html'

    def form_valid(self, form):
        form.agregarCampo()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


"""
def index(request):
    # template = loader.get_template('dbconnection/index.html')
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            # return HttpResponse(form.cleaned_data)
            output= form.send()
            return HttpResponse(output)
    else:
        form = QueryForm()
    return render(request, 'dbconnection/index.html', {'form': form})
    # return HttpResponse(template.render(context, request))
"""
