from django.urls import path
from . import views
from .views import registrar_email, aprovar_rda, excluir_provisao_gasto

urlpatterns = [
    path("",         views.home,              name="home"),
    path("iniciativas/", views.dashboard_iniciativas, name="dashboard_iniciativas"),
    path("pleitos/", views.pleitos_dashboard, name="pleitos_dash"),
    path("projetos/",views.projetos_dashboard,name="dashboard_projetos"),
    path('rda/<int:pk>/registrar-email/', registrar_email, name='registrar_email'),
    path('rda/<int:pk>/aprovar/', aprovar_rda, name='aprovar_rda'),
    path('excluir_provisao_gasto/<int:pk>/', views.excluir_provisao_gasto, name='excluir_provisao_gasto'),
]