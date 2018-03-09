from django.http import HttpResponse
from django.template import loader
from .forms import QueryForm
from django.shortcuts import render

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