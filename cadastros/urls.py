from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Agentes
    path('agentes/', views.agente_list, name='agente_list'),
    path('agentes/novo/', views.agente_create, name='agente_create'),
    path('agentes/<int:pk>/editar/', views.agente_edit, name='agente_edit'),
    path('agentes/<int:pk>/excluir/', views.agente_delete, name='agente_delete'),

    # Viaturas
    path('viaturas/', views.viatura_list, name='viatura_list'),
    path('viaturas/nova/', views.viatura_create, name='viatura_create'),
    path('viaturas/<int:pk>/editar/', views.viatura_edit, name='viatura_edit'),
    path('viaturas/<int:pk>/excluir/', views.viatura_delete, name='viatura_delete'),

    # Rastreadores
    path('rastreadores/', views.rastreador_list, name='rastreador_list'),
    path('rastreadores/novo/', views.rastreador_create, name='rastreador_create'),
    path('rastreadores/<int:pk>/editar/', views.rastreador_edit, name='rastreador_edit'),
    path('rastreadores/<int:pk>/excluir/', views.rastreador_delete, name='rastreador_delete'),

    # Armamento
    path('armamento/', views.armamento_list, name='armamento_list'),
    path('armamento/novo/', views.armamento_create, name='armamento_create'),
    path('armamento/<int:pk>/editar/', views.armamento_edit, name='armamento_edit'),
    path('armamento/<int:pk>/excluir/', views.armamento_delete, name='armamento_delete'),

    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/json/', views.clientes_json, name='clientes_json'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/excluir/', views.cliente_inativar, name='cliente_delete'),
]

# Coletes
urlpatterns += [
    path('coletes/',                 views.colete_list,   name='colete_list'),
    path('coletes/novo/',            views.colete_create, name='colete_create'),
    path('coletes/<int:pk>/editar/', views.colete_edit,   name='colete_edit'),
    path('coletes/<int:pk>/excluir/',views.colete_delete, name='colete_delete'),
]

# Equipes
urlpatterns += [
    path('operacional/equipes/',                          views.equipe_list,      name='equipe_list'),
    path('operacional/equipes/nova/',                     views.equipe_create,    name='equipe_create'),
    path('operacional/equipes/<int:pk>/editar/',          views.equipe_edit,      name='equipe_edit'),
    path('operacional/equipes/<int:pk>/excluir/',         views.equipe_delete,    name='equipe_delete'),
    path('operacional/equipes/<int:pk>/finalizar/',       views.equipe_finalizar, name='equipe_finalizar'),
]

# Ordens de Servico
urlpatterns += [
    path('operacional/os/',                              views.os_list,              name='os_list'),
    path('operacional/os/nova/',                         views.os_nova,              name='os_nova'),
    path('operacional/os/nova/detalhe/',                 views.os_detalhe_novo,      name='os_detalhe_novo'),
    path('operacional/os/<int:pk>/',                     views.os_detalhe,           name='os_detalhe'),
    path('operacional/os/<int:pk>/excluir/',             views.os_delete,            name='os_delete'),
    path('operacional/os/<int:pk>/operacional/',         views.os_operacional_save,  name='os_operacional_save'),
    path('operacional/os/<int:pk>/print/',               views.os_print,             name='os_print'),
    path('operacional/os/<int:pk>/email/',               views.os_email_html,        name='os_email_html'),
    path('operacional/os/<int:pk>/finalizar/',           views.os_finalizar,         name='os_finalizar'),
]

# Faturamento — Tabela de Precos
urlpatterns += [
    path('faturamento/tabelas/',                   views.tabela_preco_list,   name='tabela_preco_list'),
    path('faturamento/tabelas/nova/',              views.tabela_preco_create, name='tabela_preco_create'),
    path('faturamento/tabelas/<int:pk>/editar/',   views.tabela_preco_edit,   name='tabela_preco_edit'),
    path('faturamento/tabelas/<int:pk>/excluir/',  views.tabela_preco_delete, name='tabela_preco_delete'),

    # OS - Gerar/Desativar link externo
    path('operacional/os/<int:pk>/gerar-link/', views.os_gerar_link, name='os_gerar_link'),
    path('operacional/os/<int:pk>/desativar-link/', views.os_desativar_link, name='os_desativar_link'),

    # OS - Link externo do agente
    path('os/field/<uuid:token>/', views.os_field_link, name='os_field_link'),
    path('os/field/<uuid:token>/marco/salvar/', views.os_field_marco_salvar, name='os_field_marco_salvar'),

    path('os/field/<uuid:token>/foto-marco/', views.os_field_foto_marco, name='os_field_foto_marco'),
    path('os/field/<uuid:token>/foto-marco/<int:foto_pk>/delete/', views.os_field_foto_marco_delete, name='os_field_foto_marco_delete'),
    path('os/field/<uuid:token>/parada/salvar/', views.os_field_parada_salvar, name='os_field_parada_salvar'),
    path('os/field/<uuid:token>/parada/<int:pk>/delete/', views.os_field_parada_delete, name='os_field_parada_delete'),
    path('os/field/<uuid:token>/incidente/salvar/', views.os_field_incidente_salvar, name='os_field_incidente_salvar'),
    path('os/field/<uuid:token>/incidente/<int:pk>/delete/', views.os_field_incidente_delete, name='os_field_incidente_delete'),
    path('os/field/<uuid:token>/foto-veiculo/', views.os_field_foto_veiculo, name='os_field_foto_veiculo'),
    path('os/field/<uuid:token>/foto-veiculo/<int:foto_pk>/delete/', views.os_field_foto_veiculo_delete, name='os_field_foto_veiculo_delete'),
    path('os/field/<uuid:token>/troca-motorista/salvar/', views.os_field_troca_motorista, name='os_field_troca_motorista'),
    path('os/field/<uuid:token>/troca-motorista/<int:pk>/delete/', views.os_field_troca_motorista_delete, name='os_field_troca_motorista_delete'),
    path('os/field/<uuid:token>/assinatura/', views.os_field_assinatura, name='os_field_assinatura'),
    path('os/field/<uuid:token>/despesa/salvar/', views.os_field_despesa_salvar, name='os_field_despesa_salvar'),
    path('os/field/<uuid:token>/despesa/<int:pk>/delete/', views.os_field_despesa_delete, name='os_field_despesa_delete'),
    path('os/field/<uuid:token>/veiculo/salvar/', views.os_field_veiculo_salvar, name='os_field_veiculo_salvar'),
    path('os/field/<uuid:token>/veiculo/<int:pk>/delete/', views.os_field_veiculo_delete, name='os_field_veiculo_delete'),

    # Equipes
    path('operacional/equipes/', views.equipe_list, name='equipe_list'),
    path('operacional/equipes/nova/', views.equipe_create, name='equipe_create'),
    path('operacional/equipes/<int:pk>/editar/', views.equipe_edit, name='equipe_edit'),
    path('operacional/equipes/<int:pk>/excluir/', views.equipe_delete, name='equipe_delete'),
    path('operacional/equipes/<int:pk>/finalizar/', views.equipe_finalizar, name='equipe_finalizar'),

    # OS
    path('operacional/os/', views.os_list, name='os_list'),
    path('operacional/os/nova/', views.os_nova, name='os_nova'),
    path('operacional/os/<int:pk>/', views.os_detalhe, name='os_detalhe'),
    path('operacional/os/<int:pk>/excluir/', views.os_delete, name='os_delete'),
    path('operacional/os/<int:pk>/finalizar/', views.os_finalizar, name='os_finalizar'),
    path('operacional/os/<int:pk>/salvar/', views.os_operacional_save, name='os_operacional_save'),
    path('operacional/os/<int:pk>/print/', views.os_print, name='os_print'),
    path('operacional/os/<int:pk>/email/', views.os_email_html, name='os_email_html'),

    # Tabela de Precos
    path('tabelas-preco/', views.tabela_preco_list, name='tabela_preco_list'),
    path('tabelas-preco/nova/', views.tabela_preco_create, name='tabela_preco_create'),
    path('tabelas-preco/<int:pk>/editar/', views.tabela_preco_edit, name='tabela_preco_edit'),
    path('tabelas-preco/<int:pk>/excluir/', views.tabela_preco_delete, name='tabela_preco_delete'),

    # Boletim
    path('boletim/', views.boletim_list, name='boletim_list'),
    path('boletim/<int:pk>/', views.boletim_detalhe, name='boletim_detalhe'),
    path('boletim/export/pdf/', views.boletim_export_pdf, name='boletim_export_pdf'),
    path('boletim/export/xlsx/', views.boletim_export_xlsx, name='boletim_export_xlsx'),

    # Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/novo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_edit, name='usuario_edit'),
    path('usuarios/<int:pk>/senha/', views.usuario_senha, name='usuario_senha'),
    path('usuarios/<int:pk>/excluir/', views.usuario_delete, name='usuario_delete'),
]
