from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse

from .import sentimenter
from .forms import userinput
from .sentimenter import*

def index(request):
    user_input = userinput()
    return render(request, "index.html", {'input_hastag': user_input})

def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        print (input_hastag)
        data = sentimenter.primary(input_hastag)
        return render(request, "result.html", {'data': data})
    return render(request, "index.html", {'input_hastag': user_input})