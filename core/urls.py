from django.urls import path
from core import views
from core.views import *

urlpatterns = [
    path('', views.loginView, name='login_page'),
    path('base/', views.baseView, name='base_page'),
    path('logout/', views.logoutView, name='logout'),
    path('home/', views.homeView, name='home'),

    path('home/entrada_material/', views.itemAddView, name='entrada_material'),
    path('home/listar_items/editar/<int:id>/', views.editarItemsView, name='editar_items'),

    path('home/add_contrato/', views.addContratoView, name='add_contr'),
    path('home/list_all/', views.listarAllItemsView, name='listar_all'),
    path('home/list_all/more_info/<str:item>/', views.viewAllItens, name='info_itens'),

    path('home/listar_items/excluir/<int:id>/', views.excluirItems, name='excluir_item'),

    path('home/listar_items/saida_item/<int:id>/', views.saida_ItemView, name='saida_item'),
    path('create_material_saida/<int:material_tipo_id>/', views.create_material_saida, 
         name='create_material_saida'),
    
    path('home/historic_entr/', views.histUsuarioView, name='hist_usuario'),

    path('home/filtro/<int:id>/', views.filtro_view, name='filtro_view'),  

    #API views here
    path('filtro_json/', jsFiltroJson.as_view(), name='response_filtro'),
    path('response_dep/', ChartDepResponse.as_view(), name='departamentos_resp'),

    # Estatisticas view
    path('home/metricas/', views.MetricasView, name='metricas_page'),
    path('home/metricas_view/<int:dep>/<int:uni>/<str:dep_nome>/', views.count_dep, name='view_dep'),

    # Async views here
    path('home/async_view_teste/', views.teste_async, name='teste_async'),
    path('home/async_view_two/', views.teste_async_two, name='teste_async_two'),
    path('relatorio_resp/', views.relatorioResponse, name='relatorio_resp'),

    path('home/async_items/', views.dados_items, name='items_dados'),
    path('home/async_mater/', views.materiais_info, name='materiais_info'),

    path('home/buscar/', views.BuscarView, name='buscar_dados'),

    path('home/unidade/', views.UnidadeAddView, name='unidade_add'),
    path('home/departamento/', views.DepartamentoAddView, name='depart_add'),
    path('home/divisao/', views.DivisaoAddView, name='divisao_add'),

    path('retornar_excell/', views.RetornarExcell, name='retornar_excell'),

    path('home/buscar_nserie/', views.BuscarNserieView, name='buscar_nserie'),
    path('home/buscar_patri/', views.BuscarPatrimonioView, name='buscar_patri'),

    path('home/all_sem_saida/', views.all_disponiveis, name='all_disponiveis'),
    path('home/all_sem_saida/saida_view/<str:item>/', views.all_disponiveisView, name='view_sem_saida'),

    path('home/all_sem_saida/saida_many/<str:item>/', views.saida_many, name='saida_many'),
    path('home/salvar_multiplos/', views.salvar_multiplos, name='salvar_multiplos'),

    path('home/itensc_saida/', views.all_ItensExit, name='itens_csaida'),
    path('home/itensc_saida/csaida_view/<str:item>/', views.all_saidaExitView, name='itens_csaida_view'),
]

