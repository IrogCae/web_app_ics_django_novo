from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    perfil = models.CharField(max_length=50, choices=[
        ('analista', 'Analista'),
        ('coordenador', 'Coordenador'),
        ('admin', 'Administrador')
    ], default='analista')

    def __str__(self):
        return self.nome