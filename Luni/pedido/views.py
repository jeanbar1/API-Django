from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from principal.decorators import group_required
from .models import *
from .forms import *


@login_required
def listar_pedidos(request, id=None):
    
    """
    Mostra uma lista de pedidos.

    Se o parâmetro id for passado, lista os pedidos do usuário com o id especificado.
    Caso o usuário atual seja o mesmo que o especifcado em id, ou se o usuário atual
    for um administrador, lista todos os pedidos do usuário. Caso contrário, redireciona
    para a lista de pedidos do usuário atual.

    Se o parâmetro id não for passado, lista todos os pedidos se o usuário atual for
    um administrador. Caso contrário, redireciona para a lista de pedidos do usuário atual.

    :param request: Requisição do usuário.
    :param id: Id do usuário cujos pedidos devem ser listados. Se não for passado, lista
        os pedidos do usuário atual.
    :return: Uma página HTML com a lista de pedidos.
    """
    if id:
        if not request.user.is_superuser and id != request.user.pk:
            redirect('listar_pedidos', request.user.pk)
            
        user = get_object_or_404(Usuario, pk=id)
        pedidos = Pedido.objects.filter(cliente=user)
        
    elif request.user.is_superuser:
        pedidos = Pedido.objects.all()
        
    else:
        redirect('listar_pedidos', request.user.pk)
        
    return render(request, 'pedido/listar_pedidos.html', {'pedidos': pedidos})


@login_required
@group_required('Administradores')
def create_pedido(request):
    """
    Cria um novo pedido.

    Requer permissão de Administrador.

    :param request: Requisição do usu´srio.
    :return: Redireciona para a página de listagem de pedidos.
    """
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pedido/')
        else:
            return render(request, "form.html", {"form" : form, 'titulo' : 'Criar pedido'})
    else:
        form = PedidoForm()
        return render(request, "form.html", {"form" : form, 'titulo' : 'Criar pedido'})
    

@login_required
@group_required('Administradores')
def edit_pedido(request, id):
    """
    Edita um pedido pelo id.

    Requer permiss o de Administrador.

    :param request: Requisição do usuário.
    :param id: Id do pedido a ser editado.
    :return: Redireciona para a página de listagem de pedidos.
    """
    
    pedido = Pedido.objects.get(pk = id)
    print(pedido)

    if request.method == "POST":
        form = PedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()

            return redirect('/pedido/')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'form.html', {'form' : form, 'titulo': 'Editar pedido'})


@login_required
@group_required('Administradores')
def remove_pedido(request, id):
    """
    Remove um pedido pelo id.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :param id: Id do pedido a ser removida.
    :return: Redireciona para a página de listagem de pedidos.
    """
    pedido = Pedido.objects.filter(pk=id).first()
    
    if not pedido:
        messages.error(request, 'Pedido não encontrado.')
        return redirect("listar_pedidos")

    pedido.delete()
    return redirect('listar_pedidos')


@login_required
def pedido(request, id):
    """
    Renderiza a página do pedido com o id fornecido.
    
    Se o pedido não existir, redireciona para a página de listagem de pedidos com uma mensagem de erro.
    Se o usuário logado for o dono do pedido ou um administrador, renderiza a página de detalhes do pedido.
    Caso contrário, redireciona para a página de listagem de pedidos com uma mensagem de erro.
    """
    pedido = Pedido.objects.filter(pk=id).first()
    
    if not pedido:
        messages.error(request, 'Pedido não encontrado.')
        return redirect("listar_pedidos")

    if request.user.is_superuser or request.user.id == pedido.cliente.id:
        itens = ItemPedido.objects.filter(pedido=pedido)
        return render(request, 'pedido/pedido.html', {'pedido': pedido, 'itens': itens})
    
    messages.error(request, 'Você não tem permissão para acessar esta página.')
    return redirect("listar_pedidos")