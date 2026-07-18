from django.shortcuts import render, get_object_or_404, redirect
from .models import Demanda
from .forms import DemandaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def home(request):
    demandas = Demanda.objects.filter(status="ABERTA").order_by("-criada_em")
    return render(request, "core/index.html", {"demandas": demandas})

@login_required
def criar_demanda(request):
    if request.user.tipo != "CLIENTE":
        raise PermissionDenied
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

@login_required
def editar_demanda(request, pk):
    demanda = get_object_or_404(Demanda, pk=pk)
    if demanda.cliente != request.user:
        raise PermissionDenied
    
    if request.method == "POST":
        form = DemandaForm(request.POST, instance=demanda)
        if form.is_valid():
            form.save()
            messages.success(request, "Demanda atualizada com sucesso!")
            return redirect("detalhe_demanda", pk=demanda.pk)
    else:
        form = DemandaForm(instance=demanda)

    return render(request, "core/criar_demanda.html", {"form": form})

@login_required
def excluir_demanda(request, pk):
    demanda = get_object_or_404(Demanda, pk=pk)
    if demanda.cliente != request.user:
        raise PermissionDenied
    if request.method == "POST":
        demanda.delete()
        messages.success(request, "Demanda excluída com sucesso!")
        return redirect("home")

    return render(request, "core/excluir_demanda.html", {"demanda": demanda})

def sobre(request):
    return render(request, "core/sobre.html")

