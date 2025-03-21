from django.urls import include, path
from core import views

urlpatterns = [
    path('', views.loginView, name='login_page'),
    path('base/', views.baseView, name='base_page'),
]
