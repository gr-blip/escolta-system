"""
cadastros/models_perfil.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Perfil de usuário com níveis de acesso:
  developer  → acesso total + oculto nas listagens
  admin      → acesso total visível
  operador   → acesso operacional comum
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTRUÇÕES DE USO:
  1. Cole este conteúdo ao final do seu models.py existente
     (ou em um arquivo separado e importe em models.py)
  2. Rode: python manage.py makemigrations && python manage.py migrate
  3. Para criar os usuários, use o management command: criar_usuarios
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    NIVEL_CHOICES = [
        ('developer', 'Developer'),
        ('admin',     'Administrador'),
        ('operador',  'Operador'),
    ]

    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nivel  = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='operador', verbose_name='Nível de Acesso')
    oculto = models.BooleanField(default=False, verbose_name='Usuário Oculto',
                                  help_text='Se marcado, não aparece em listagens de usuários')

    class Meta:
        verbose_name        = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return f'{self.user.username} [{self.get_nivel_display()}]'

    @property
    def is_developer(self):
        return self.nivel == 'developer'

    @property
    def is_admin(self):
        return self.nivel in ('developer', 'admin')


# Cria automaticamente o perfil quando um User é criado
@receiver(post_save, sender=User)
def criar_perfil_automatico(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def salvar_perfil_automatico(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
