from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("<h1> HOLA MUNDO! </h1>")

def cotizacionCl(request):
    return render(request, 'cotizacionCl.html')