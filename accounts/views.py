from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CadastroForm
# Create your views here.
def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # ja loga o usuário
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("home")
    else:
        form = CadastroForm()

    return render(request, "accounts/cadastro.html", {"form": form})