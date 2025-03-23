from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login

from principal.decorators import group_required
from .models import *
from .forms import *

def create_usuario(request):
    """
    Cria um novo usuário.

    Se o request for POST, salva o formulário e faz o login com o novo usuário.
    Se o request for GET, renderiza o formulário de cadastro com um novo usuário.

    :param request: Requisição do HTTP
    :return: Uma página de redirecionamento para a página inicial ou a página de cadastro
    """
    if request.method == "POST":
        form = UsuarioFormSingup(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST.get('password1'))
            user.save()
            
            login(request, user)
            grupo, created = Group.objects.get_or_create(name='Clientes')
            
            user.groups.add(grupo)
            return redirect('home')
        else:
            return render(request, "registration/cadastro.html", {"form" : form, 'titulo' : 'Criar Usuário'})
    else:
        form = UsuarioFormSingup()
        return render(request, "registration/cadastro.html", {"form" : form, 'titulo' : 'Criar Usuário'})
    

@login_required
def edit_usuario(request, id):
    """
    Edita um usuário pelo id.

    Se o request for POST, salva o formulário e faz o login com o usuário editado.
    Se o request for GET, renderiza o formulário de edição com o usuário
    correspondente ao id.

    :param request: Requisição do HTTP
    :param id: Id do usuário a ser editado
    :return: Uma página de redirecionamento para a página de perfil do usuário
    """
    if not request.user.is_superuser and id != request.user.id:
        return redirect('perfil_usuario')
        
    usuario = Usuario.objects.filter(pk = id).first()

    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)

        if form.is_valid():
            user = form.save()
            
            if request.user.id == usuario.id:
                login(request, user)
            
            return redirect('perfil_usuario', id=id)
    else:
        form = UsuarioForm(instance=usuario)
    
    context = {'form' : form, 'titulo' : 'Editar Usuário'}
    
    if usuario.imagem and hasattr(usuario.imagem, 'url'):
        context['current_image_url'] = usuario.imagem.url
    
    return render(request, 'form.html', context)


@login_required
@group_required('Administradores')
def remove_usuario(request, id):
    """
    Remove um usuário pelo id.

    Requer permissão de Administrador.

    :param request: Requisição do HTTP
    :param id: Id do usuário a ser deletado
    :return: Uma página de redirecionamento para a página de listagem de usuários
    """
    usuario = Usuario.objects.filter(pk = id).first()
    
    if usuario: usuario.delete()

    return redirect('listar_usuarios')


@login_required
def perfil(request, id=None):
    """
    Página de perfil do usuário.

    Se o usuário não for administrador e tentar acessar o perfil de outro usuário,
    redireciona para o perfil do usuário logado.

    :param request: Requisição do HTTP
    :param id: Opcional, id do usuário a ser visualizado. Se não for passado,
               redireciona para o perfil do usuário logado.
    :return: Uma página renderizada com o perfil do usuário
    """
    if not request.user.is_superuser and id is not None and id != request.user.id:
        return redirect('perfil_usuario')
    
    user = None
    if id:
        user = get_object_or_404(Usuario, pk=id)
    else:
        user = request.user
    
    form = UsuarioForm(instance=user)
    
    return render(request, 'usuario/perfil.html', {'form': form, 'user': user, 'titulo' : 'Perfil do Usuário'})


@login_required
@group_required('Administradores')
def mudar_tipo(request, id):
    """
    Muda o tipo do usuário pelo id.

    Requer permissão de Administrador.

    :param request: Requisição do HTTP
    :param id: Id do usuário a ter o tipo mudado
    :return: Uma página de redirecionamento para a página de perfil do usuário
    """
    if request.method == "POST":
        tipo = request.POST.get('tipo', "Cliente")
        user = get_object_or_404(Usuario, pk=id)

        if tipo == "CLIENTE":
            user.groups.clear()
            user.is_superuser = False
            user.tipo_cliente = tipo
            grupo, created = Group.objects.get_or_create(name='Clientes')
            user.groups.add(grupo)

        elif tipo == "ADMINISTRADOR":
            user.groups.clear()
            user.tipo_cliente = tipo
            user.is_superuser = True
            grupo, created = Group.objects.get_or_create(name='Administradores')
            user.groups.add(grupo)
            
        elif tipo == "CORPORATIVO":
            user.groups.clear()
            user.is_superuser = False
            user.tipo_cliente = tipo
            grupo, created = Group.objects.get_or_create(name='Corporativos')
            user.groups.add(grupo)
            
        user.save()
        messages.success(request, f"Tipo de usuário alterado com sucesso para {Usuario.TIPOS_CLIENTE_DICT[tipo]}.")
    
    return redirect('perfil_usuario', id=id)


@login_required
@group_required('Administradores')
def listar_usuarios(request):
    """
    Mostra uma lista de todos os usuários.

    Requer permissão de Administrador.

    :param request: Requisição do HTTP
    :return: Uma página HTML com a lista de usuários.
    """
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/listar_usuarios.html', {'usuarios': usuarios})


def receber_suporte_corporativo(request):
    """
    Mostra uma página para os usuários corporativos.

    Se o usuário for administrador, renderiza a página de suporte corporativo.
    Senão, exibe uma mensagem de erro e redireciona para a página inicial.

    :param request: Requisição do HTTP
    :return: Uma página HTML de suporte corporativo ou uma página de erro.
    """
    if request.user.groups.filter(name='Administradores').exists():
        return render(request, 'support/receber_suporte_corporativo.html')
    
    messages.error(request, 'Você não tem permissão para acessar esta página. Para ter uma conta corporativa entre em contato com luni.support@gmail.com')
    
    return redirect('home')