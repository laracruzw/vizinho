from django.test import TestCase

# Create your tests here.
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Demanda, Orcamento

User = get_user_model()


class DemandaTests(TestCase):
    def setUp(self):
        self.cliente = User.objects.create_user(
            username="cliente_teste", password="senha123", tipo="CLIENTE"
        )
        self.mei = User.objects.create_user(
            username="mei_teste", password="senha123", tipo="MEI"
        )
        self.demanda = Demanda.objects.create(
            cliente=self.cliente,
            titulo="Trocar tomada",
            descricao="Tomada queimada",
            categoria="ELETRICA",
            cidade="Florianópolis",
        )

    def test_demanda_nasce_aberta(self):
        self.assertEqual(self.demanda.status, "ABERTA")

    def test_criar_demanda_exige_login(self):
        resposta = self.client.get(reverse("criar_demanda"))
        self.assertEqual(resposta.status_code, 302)

    def test_mei_nao_cria_demanda(self):
        self.client.login(username="mei_teste", password="senha123")
        resposta = self.client.get(reverse("criar_demanda"))
        self.assertEqual(resposta.status_code, 403)

    def test_nao_dono_nao_edita(self):
        self.client.login(username="mei_teste", password="senha123")
        resposta = self.client.get(reverse("editar_demanda", args=[self.demanda.pk]))
        self.assertEqual(resposta.status_code, 403)


class OrcamentoTests(TestCase):
    def setUp(self):
        self.cliente = User.objects.create_user(
            username="cliente_teste", password="senha123", tipo="CLIENTE"
        )
        self.mei = User.objects.create_user(
            username="mei_teste", password="senha123", tipo="MEI"
        )
        self.demanda = Demanda.objects.create(
            cliente=self.cliente,
            titulo="Pintar parede",
            descricao="Sala inteira",
            categoria="PINTURA",
            cidade="Florianópolis",
        )

    def test_orcamento_duplicado_falha(self):
        Orcamento.objects.create(
            demanda=self.demanda, mei=self.mei, valor=Decimal("200.00"), mensagem="Faço"
        )
        with self.assertRaises(IntegrityError):
            Orcamento.objects.create(
                demanda=self.demanda, mei=self.mei, valor=Decimal("300.00"), mensagem="De novo"
            )

    def test_aceitar_fecha_demanda(self):
        orcamento = Orcamento.objects.create(
            demanda=self.demanda, mei=self.mei, valor=Decimal("200.00"), mensagem="Faço"
        )
        self.client.login(username="cliente_teste", password="senha123")
        self.client.post(reverse("aceitar_orcamento_ajax", args=[orcamento.pk]))

        orcamento.refresh_from_db()
        self.demanda.refresh_from_db()
        self.assertTrue(orcamento.aceito)
        self.assertEqual(self.demanda.status, "FECHADA")