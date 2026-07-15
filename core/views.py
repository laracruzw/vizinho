from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def home(request):
    demandas = [
        {"titulo": "Trocar tomada queimada", "categoria": "Elétrica", "cidade": "Florianópolis"},
        {"titulo": "Pintar quarto pequeno", "categoria": "Pintura", "cidade": "São José"},
        {"titulo": "Consertar vazamento na pia", "categoria": "Hidráulica", "cidade": "Palhoça"},
    ]
    return render(request, "core/index.html", {"demandas": demandas}) 
    # passa dados pro template via dict

def sobre(request):
    return HttpResponse("Página sobre o projeto.")