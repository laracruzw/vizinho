from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def home(request):
    return render(request, "core/index.html")

def sobre(request):
    return HttpResponse("Página sobre o projeto.")