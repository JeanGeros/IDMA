from django.shortcuts import render
from django.template.loader import get_template
from django.template import loader
# Create your views here.

def Prueba(request):
    return render(request, 'prueba.html') 