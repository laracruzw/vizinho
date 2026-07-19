from django import forms
from .models import Demanda, Orcamento


class DemandaForm(forms.ModelForm):
    class Meta:
        model = Demanda
        fields = ["titulo", "descricao", "categoria", "cidade"]

class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ["valor", "mensagem"]