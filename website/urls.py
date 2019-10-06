from . import views
from django.urls import path

app_name = 'website'

urlpatterns = [
    # GET /
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('funcionarios/', views.FuncionarioListView, name='lista_funcionarios'),
    path('funcionario/<pk>',views.FuncionarioUpdateView.as_view(), name='atualiza_funcionario'),
    path('funcionario/excluir/<pk>', views.FuncionarioDeleteView.as_view(), name='deleta_funcionario'),
    path('funcionario/cadastrar/', views.FuncionarioCreateView, name='cadastra_funcionario'),
    path('registrar/', views.register, name='registrar'),
    path('logout/', views.request_logout, name='logout'),
    path('login/', views.request_login, name='login')
]