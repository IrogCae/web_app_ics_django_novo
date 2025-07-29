# accounts/admin.py

from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'perfil', 'ativo']
    search_fields = ['nome', 'email']
    list_filter = ['perfil', 'ativo']