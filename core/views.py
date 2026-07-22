from django.shortcuts import render, get_object_or_404, redirect
from .models import Demanda, Orcamento
from .forms import DemandaForm, OrcamentoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

def home(request):
    demandas = Demanda.objects.filter(status="ABERTA")

    categoria = request.GET.get("categoria")
    cidade = request.GET.get("cidade")

    if categoria:
        demandas = demandas.filter(categoria=categoria)

    if cidade:
        demandas = demandas.filter(cidade__icontains=cidade)

    demandas = demandas.order_by("-criada_em")

    return render(request, "core/index.html", {
        "demandas": demandas,
        "categorias": Demanda.Categoria.choices,
    })

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
    orcamentos = demanda.orcamentos.select_related("mei").order_by("valor")
    return render(request, "core/detalhe.html", {
        "demanda": demanda,
        "orcamentos": orcamentos,
    })

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

@login_required
def minhas_demandas(request):
    if request.user.tipo != "CLIENTE":
        raise PermissionDenied
    demandas = Demanda.objects.filter(cliente=request.user).order_by("-criada_em")
    return render(request, "core/minhas_demandas.html", {"demandas": demandas})

@login_required
def enviar_orcamento(request, pk):
    demanda = get_object_or_404(Demanda, pk=pk)

    if request.user.tipo != "MEI":
        raise PermissionDenied

    if demanda.status != "ABERTA":
        messages.error(request, "Esta demanda não está mais aberta.")
        return redirect("detalhe_demanda", pk=demanda.pk)

    if Orcamento.objects.filter(demanda=demanda, mei=request.user).exists():
        messages.error(request, "Você já enviou um orçamento para esta demanda.")
        return redirect("detalhe_demanda", pk=demanda.pk)

    if request.method == "POST":
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save(commit=False)
            orcamento.demanda = demanda
            orcamento.mei = request.user
            orcamento.save()
            messages.success(request, "Orçamento enviado com sucesso!")
            return redirect("detalhe_demanda", pk=demanda.pk)
    else:
        form = OrcamentoForm()

    return render(request, "core/enviar_orcamento.html", {"form": form, "demanda": demanda})

@login_required
def aceitar_orcamento(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    demanda = orcamento.demanda

    if demanda.cliente != request.user:
        raise PermissionDenied

    if demanda.status != "ABERTA":
        messages.error(request, "Esta demanda já foi fechada.")
        return redirect("detalhe_demanda", pk=demanda.pk)

    if request.method == "POST":
        orcamento.aceito = True
        orcamento.save()

        demanda.status = "FECHADA"
        demanda.save()

        messages.success(request, f"Orçamento de {orcamento.mei.username} aceito!")

    return redirect("detalhe_demanda", pk=demanda.pk)

@login_required
def meus_orcamentos(request):
    if request.user.tipo != "MEI":
        raise PermissionDenied

    orcamentos = request.user.orcamentos_enviados.select_related("demanda").order_by("-criado_em")
    return render(request, "core/meus_orcamentos.html", {"orcamentos": orcamentos})

@login_required
def aceitar_orcamento_ajax(request, pk):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    orcamento = get_object_or_404(Orcamento, pk=pk)
    demanda = orcamento.demanda

    if demanda.cliente != request.user:
        return JsonResponse({"erro": "Sem permissão"}, status=403)

    if demanda.status != "ABERTA":
        return JsonResponse({"erro": "Demanda já fechada"}, status=400)

    orcamento.aceito = True
    orcamento.save()
    demanda.status = "FECHADA"
    demanda.save()

    return JsonResponse({
        "ok": True,
        "mei": orcamento.mei.username,
        "valor": str(orcamento.valor),
    })