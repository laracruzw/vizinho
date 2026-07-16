from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # "": endereço, views.home é a funct que responde,
    #  name é o apelido pra essa rota
    path("demanda/<int:pk>/", views.detalhe_demanda, name="detalhe_demanda"),
]