from django.urls import path
from . import views
from .views import (
    CreateUsuarioAPIView,
    EditUsuarioAPIView,
    RemoveUsuarioAPIView,
    PerfilUsuarioAPIView,
    ListarUsuariosAPIView,
    MudarTipoUsuarioAPIView,
)


urlpatterns = [
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'), # lista de usuários
    path('<int:id>/mudar_tipo/', views.mudar_tipo, name='mudar_tipo'), # muda o tipo de usuário
    path('perfil/<int:id>/', views.perfil, name='perfil_usuario'), # perfil do usuário
    path('perfil/', views.perfil, name='perfil_usuario'), # perfil do usuário
    path('create/', views.create_usuario, name='create_usuario'), # cria um novo usuário
    path('update/<int:id>/', views.edit_usuario, name='edit_usuario'), # edita um usuário
    path('delete/<int:id>/', views.remove_usuario, name='delete_usuario'), # remove um usuário
    path('receber_suporte_corporativo/', views.receber_suporte_corporativo, name='receber_suporte_corporativo'), # TODO: recebe suporte


    # Novas URLs para a API
    path('usuarios/create/', CreateUsuarioAPIView.as_view(), name='create-usuario'),
    path('usuarios/edit/<int:id>/', EditUsuarioAPIView.as_view(), name='edit-usuario'),
    path('usuarios/delete/<int:id>/', RemoveUsuarioAPIView.as_view(), name='remove-usuario'),
    path('usuarios/perfil/', PerfilUsuarioAPIView.as_view(), name='perfil-usuario'),
    path('usuarios/perfil/<int:id>/', PerfilUsuarioAPIView.as_view(), name='perfil-usuario-id'),
    path('usuarios/', ListarUsuariosAPIView.as_view(), name='listar-usuarios'),
    path('usuarios/mudar-tipo/<int:id>/', MudarTipoUsuarioAPIView.as_view(), name='mudar-tipo-usuario'),
]