from django.urls import include, path
from core import views

urlpatterns = [
    path('', views.loginView, name='login_page'),
    path('base/', views.baseView, name='base_page'),
    path('logout/', views.logoutView, name='logout'),
    path('home/', views.homeView, name='home'),
    path('inse_item/', views.inserirItem, name='new_item'),
    path('home/entrada_material/', views.itemSaidaView, name='entrada_material'),
    path('home/listar_items/editar/<int:id>/', views.editarItemsView, name='editar_items'),

    path('home/add_contrato/', views.addContratoView, name='add_contr'),
    path('home/listar_items/', views.listarItemsView, name='listar_items'),
    path('home/addUnidade/', views.addUnidadeView, name='add_unidade'),

    path('home/listar_items/excluir/<int:id>/', views.excluirItems, name='excluir_item'),
]

