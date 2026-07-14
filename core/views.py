from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("Olá, esta é a home do Vizinho de Aluguel!")

def sobre(request):
    return HttpResponse("Página sobre o projeto.")