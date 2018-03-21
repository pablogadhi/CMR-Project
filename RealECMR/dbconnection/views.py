from django.http import HttpResponse
from django.template import loader
from .forms import QueryForm
from django.shortcuts import render
from .models import Cliente, Propietario,Comprador, Propiedad, Intermediario
from django.views import generic

def index(request):
    num_propietarios=Propietario.objects.all().count()
    num_compradores=Comprador.objects.all().count()
    num_propiedades=Propiedad.objects.all().count()
    num_intermediarios=Intermediario.objects.all().count()
    return render (
        request,
        'index.html',
        context={'num_propietarios':num_propietarios,'num_compradores':num_compradores,'num_propiedades':num_propiedades,'num_intermediarios':num_intermediarios},
    )

class PropetarioListView(generic.ListView):
    """
    Generic class-based view for a list of Propietario.
    """
    model = Propietario
    paginate_by = 10

class IntermediarioListView(generic.ListView):
    """
    Generic class-based view for a list of Intermediario.
    """
    model = Intermediario
    paginate_by = 10

class CompradorListView(generic.ListView):
    """
    Generic class-based view for a list of Comprador.
    """
    model = Comprador
    paginate_by = 10

class PropiedadListView(generic.ListView):
    """
    Generic class-based view for a list of Propiedad.
    """
    model = Propiedad
    paginate_by = 10

class PropiedadDetailView(generic.ListView):
    """
    Generic class-based detail for a list of Propiedad.
    """
    model = Propiedad



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