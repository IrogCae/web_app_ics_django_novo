from django.urls import path
from . import views
from .views import registrar_email, aprovar_rda, excluir_provisao_gasto, dados_grafico_iniciativas, excluir_iniciativa

urlpatterns = [
    path("",         views.home,              name="home"),
    
    path("pleitos/", views.pleitos_dashboard, name="pleitos_dash"),
    path("projetos/",views.projetos_dashboard,name="dashboard_projetos"),
    path('iniciativas/', views.iniciativas_dash, name='iniciativas_dash'),
    path('dados_grafico_iniciativas/', dados_grafico_iniciativas, name='dados_grafico_iniciativas'),

    path('rda/<int:pk>/registrar-email/', registrar_email, name='registrar_email'),
    path('rda/<int:pk>/aprovar/', aprovar_rda, name='aprovar_rda'),
    path('excluir_provisao_gasto/<int:pk>/', excluir_provisao_gasto, name='excluir_provisao_gasto'),

    path('excluir_iniciativa/<int:pk>/', excluir_iniciativa, name='excluir_iniciativa'),
]