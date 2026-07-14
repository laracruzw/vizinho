from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # "": endereço, views.home é a funct que responde,
    path("sobre/", views.sobre, name="sobre"), #  name é o apelido pra essa rota
]