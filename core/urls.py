from django.urls import include, path
from core import views

urlpatterns = [
    path('', views.loginView, name='login_page'),
    path('base/', views.baseView, name='base_page'),
    path('logout/', views.logoutView, name='logout'),
    path('home/', views.homeView, name='home'),
    path('inse_item/', views.inserirItem, name='new_item'),

    path('home/add_contrato/', views.addContratoView, name='add_contr'),
    path('home/listar_items/', views.listarView, name='listar_contr'),
    path('home/addUnidade/', views.addUnidadeView, name='add_unidade'),
]

