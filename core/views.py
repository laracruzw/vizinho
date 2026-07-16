from django.shortcuts import render, get_object_or_404, redirect
from .models import Demanda
from .forms import DemandaForm
from django.contrib import messages

def home(request):
    demandas = Demanda.objects.filter(status="ABERTA").order_by("-criada_em")
    return render(request, "core/index.html", {"demandas": demandas})

def criar_demanda(request):
    if request.method == "POST":
        form = DemandaForm(request.POST)
        if form.is_valid():
            demanda = form.save(commit=False)
            demanda.cliente = request.user
            demanda.save()
            messages.success(request, "Demanda publicada com sucesso!")
            return redirect("detalhe_demanda", pk=demanda.pk)
    else:
        form = DemandaForm()
    return render(request, "core/criar_demanda.html", {"form": form})

def detalhe_demanda(request, pk): # pk é o id da demanda
    demanda = get_object_or_404(Demanda, pk=pk)
    return render(request, "core/detalhe.html", {"demanda": demanda})

def sobre(request):
    return render(request, "core/sobre.html")

