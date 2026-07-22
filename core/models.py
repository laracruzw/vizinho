from django.conf import settings
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

class Demanda(models.Model):
    class Categoria(models.TextChoices):
        ELETRICA = "ELETRICA", "Elétrica"
        HIDRAULICA = "HIDRAULICA", "Hidráulica"
        PINTURA = "PINTURA", "Pintura"
        LIMPEZA = "LIMPEZA", "Limpeza"
        OUTROS = "OUTROS", "Outros"

    class Status(models.TextChoices):
        ABERTA = "ABERTA", "Aberta"
        FECHADA = "FECHADA", "Fechada"
        CONCLUIDA = "CONCLUIDA", "Concluída"

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, # indica que a demanda pertence a um cliente
        on_delete=models.CASCADE, # on delete indica se a demanda deve ser deletada caso o cliente seja deletado
        related_name="demandas", # related_name indica o nome do atributo que será usado para acessar as demandas do cliente
    )
    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    categoria = models.CharField(max_length=15, choices=Categoria.choices)
    cidade = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ABERTA)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo # retorna o título da demanda quando o objeto é convertido para string
    
class Orcamento(models.Model):
    demanda = models.ForeignKey(
        Demanda,
        on_delete=models.CASCADE,
        related_name="orcamentos",
    )
    mei = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orcamentos_enviados",
    )
    valor = valor = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    mensagem = models.TextField()
    aceito = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["demanda", "mei"],
                name="um_orcamento_por_mei_por_demanda",
            )
        ]

    def __str__(self):
        return f"{self.mei.username} - R$ {self.valor}"
