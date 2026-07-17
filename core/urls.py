from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # "": endereço, views.home é a funct que responde,
    #  name é o apelido pra essa rota
    path("demanda/nova/", views.criar_demanda, name="criar_demanda"),
    path("demanda/<int:pk>/editar/", views.editar_demanda, name="editar_demanda"),
    path("demanda/<int:pk>/excluir/", views.excluir_demanda, name="excluir_demanda"),
    path("demanda/<int:pk>/", views.detalhe_demanda, name="detalhe_demanda"),
    path("sobre/", views.sobre, name="sobre"),
]