from django.shortcuts import get_object_or_404, render
from .models import Demanda


def home(request):
    demandas = Demanda.objects.filter(status="ABERTA").order_by("-criada_em")
    return render(request, "core/index.html", {"demandas": demandas})

def detalhe_demanda(request, pk): # pk é o id da demanda
    demanda = get_object_or_404(Demanda, pk=pk)
    return render(request, "core/detalhe.html", {"demanda": demanda})

def sobre(request):
    return render(request, "core/sobre.html")