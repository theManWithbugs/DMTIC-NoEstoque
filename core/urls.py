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
    path('home/listar_items/', views.listarItemsView, name='listar_items'),
    path('home/list_all/', views.listarAllItemsView, name='listar_all'),
    path('home/addUnidade/', views.addUnidadeView, name='add_unidade'),

    path('home/listar_items/excluir/<int:id>/', views.excluirItems, name='excluir_item'),

    path('home/listar_items/saida_item/<int:id>/', views.saida_ItemView, name='saida_item'),
    path('create_material_saida/<int:material_tipo_id>/', views.create_material_saida, name='create_material_saida'),
    
    path('home/listar_items/listar_saida/', views.itemSaidaViewLista, name='items_saida'),
    path('home/historic_entr/', views.histUsuarioView, name='hist_usuario'),

    path('home/filtro/<int:id>/', views.filtro_view, name='filtro_view'),  
    path('home/itens_dispo/', views.noExitItemsView, name='itens_disponiveis'),

    #API views here
    path('filtro_json/', jsFiltroJson.as_view(), name='response_filtro'),
    path('response_dep/', ChartDepResponse.as_view(), name='departamentos_resp'),

    # Estatisticas view
    path('home/estatisticas/', views.EstatisticasView, name='estatisticas_page'),
    path('home/metricas/', views.MetricasView, name='metricas_page'),
    path('home/estatisticas/charts/', views.ChartsView, name='charts_page'),

    # Async views here
    path('home/async_view_teste/', views.teste_async, name='teste_async'),
    path('home/async_view_two/', views.teste_async_two, name='teste_async_two'),
    path('relatorio_resp/', views.relatorioResponse, name='relatorio_resp'),

    path('home/async_items/', views.dados_items, name='items_dados'),
    path('home/async_mater/', views.materiais_info, name='materiais_info'),

    path('home/buscar/', views.BuscarView, name='buscar_dados'),

    path('home/unidade/', views.UnidadeAddView, name='unidade_add'),
]

