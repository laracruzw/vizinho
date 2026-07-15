from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Tipo(models.TextChoices):
        CLIENTE = "CLIENTE", "Cliente"
        MEI = "MEI", "MEI"

    tipo = models.CharField(max_length=10, choices=Tipo.choices)