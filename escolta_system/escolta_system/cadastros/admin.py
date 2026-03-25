from django.contrib import admin
from .models import Agente, Viatura, Rastreador, Armamento, Cliente


@admin.register(Agente)
class AgenteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'funcao', 'status', 'cnh_validade', 'cnv_validade']
    list_filter = ['status', 'funcao']
    search_fields = ['nome', 'cpf', 'rg']


@admin.register(Viatura)
class ViaturaAdmin(admin.ModelAdmin):
    list_display = ['placa', 'marca_modelo', 'cor', 'frota', 'status']
    list_filter = ['status']
    search_fields = ['placa', 'marca_modelo', 'frota']


@admin.register(Rastreador)
class RastreadorAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'numero_serie', 'status']
    list_filter = ['status']
    search_fields = ['numero_serie', 'marca', 'modelo']


@admin.register(Armamento)
class ArmamentoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'marca', 'modelo', 'calibre', 'numero_serie', 'registro_cr']
    list_filter = ['tipo']
    search_fields = ['numero_serie', 'registro_cr', 'marca']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'cidade_uf']
    search_fields = ['razao_social', 'cnpj']


from .models import Colete

@admin.register(Colete)
class ColeteAdmin(admin.ModelAdmin):
    list_display = ['marca', 'numeracao', 'protecao', 'validade']
    list_filter = ['protecao']
    search_fields = ['marca', 'numeracao']
