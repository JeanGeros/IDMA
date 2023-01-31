from django.shortcuts import render
from django.template.loader import get_template
from django.template import loader
# Create your views here.

def Prueba(request):
    print("a")
    return render(request, 'prueba.html') 