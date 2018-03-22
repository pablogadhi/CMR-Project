from django.http import HttpResponse
from django.template import loader
from .forms import AgregarCampoForm, AgregarPropiedad
from django.shortcuts import render, get_object_or_404
from .models import Cliente, Propietario, Comprador, Propiedad, Intermediario, CamposAdicionales
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


class PropetarioListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    model = Propietario
    paginate_by = 10


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

    def get_success_url(self):
        return reverse('compradores')

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 2")
        context = super().get_context_data(**kwargs)
        context['campos_adicionales'] = dictfetchall(cursor)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.agregarCampo(2)
        return super().form_valid(form)


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
        cursor.execute(
            "SELECT * FROM dbconnection_camposadicionales as ca WHERE ca.tabla = 0")
        context = super().get_context_data(**kwargs)
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
