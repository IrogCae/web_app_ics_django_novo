# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Usuario

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Usuario.objects.get(nome=username, ativo=True)
        except Usuario.DoesNotExist:
            return None

        # compara a senha em texto puro
        if usuario.senha == password:
            # cria ou recupera o User interno do Django
            user, created = User.objects.get_or_create(
                username=usuario.nome,
                defaults={'email': usuario.email}
            )
            if created:
                # só no momento da criação, grava o hash igual à senha atual
                user.set_password(password)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
