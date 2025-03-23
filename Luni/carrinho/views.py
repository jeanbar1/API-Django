from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from pedido.models import Pedido, ItemPedido
from usuario.models import Usuario
from .models import Carrinho, ItemCarrinho

@login_required
def carrinho(request, id=None):
    """
    Mostra o carrinho de compras de um usuário.

    Se o usuário for administrador, pode visualizar o carrinho de outro usuário
    passando o id do usuário como parâmetro.

    :param request: Requisição do HTTP
    :param id: Id do usuário cujo carrinho deve ser mostrado
    :return: Uma página HTML com o carrinho de compras do usuário
    """

    if id is None:
        user = request.user
    elif request.user.is_superuser:
        user = get_object_or_404(Usuario, pk=id)
    else:
        redirect('carrinho')
    
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=Carrinho.objects.filter(usuario=user).first())
    
    context = {
        'user': user,
        'itens_carrinho': [
            {
                'item': item,
                'total_item': item.quantidade * item.produto.preco
            }
            for item in itens_carrinho
        ],
        'total': sum(item.quantidade * item.produto.preco for item in itens_carrinho)
    }
    
    return render(request, 'produto/carrinho.html', context)


@require_POST
@login_required
def atualizar_carrinho(request):
    """
    Atualiza o carrinho de compras do usuário com base em dados
    enviados via POST.

    :param request: Requisição do HTTP
    :return: Uma página de redirecionamento para a página do carrinho
    """
    for key, value in request.POST.items():
        if key.startswith('quantidade_'):
            item_id = key.split('_')[1]
            quantidade = int(value)
            item = ItemCarrinho.objects.get(id=item_id)
            
            if item.carrinho.usuario.id == request.user.id:
                item.quantidade = quantidade
                item.save()
                
    messages.success(request, 'Carrinho atualizado com sucesso.')
    return redirect('carrinho')


@require_http_methods(["GET", "POST"])
def confirmar_compra(request):
    """
    Confirma a compra do carrinho de compras do usuário.

    Se o request for POST, cria um objeto Pedido com os dados do carrinho,
    deleta os itens do carrinho e redireciona para a página de pedidos.
    Se o request for GET, renderiza a página de confirmação de compra com
    os dados do carrinho.

    :param request: Requisição do HTTP
    :return: Uma página de redirecionamento para a página de pedidos ou a página de confirmação de compra
    """
    if request.method == "POST":
        usuario = request.user
        carrinho = Carrinho.objects.get(usuario=usuario)
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)

        pedido = Pedido.objects.create(
            cliente=usuario,
            preco_total=sum(item.quantidade * item.produto.preco for item in itens_carrinho)
        )
        
        for item in itens_carrinho:
            ItemPedido.objects.create(
                estampa=item.estampa,
                tamanho=item.tamanho,
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco=item.produto.preco
            )
        
        itens_carrinho.delete()

        messages.success(request, 'Compra finalizada com sucesso!')
        return redirect('listar_pedidos')
    
    else:
        usuario = request.user
        carrinho = Carrinho.objects.get(usuario=usuario)
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)

        quantidade_total = 0
        for item in itens_carrinho:
            quantidade = int(request.GET.get(f'quantidade_{item.id}', 0))
            if quantidade > 0:
                item.quantidade = quantidade
                item.save()
                quantidade_total += quantidade
            else:
                messages.error(request, f"Quantidades inválidas. {item.produto.nome} {item.quantidade} quantidade_{item.id}")
                print(f"Quantidades inválidas. {item.produto.nome} {item.quantidade} quantidade_{item.id}")
                return redirect('carrinho')
        
        context = {
            'itens_carrinho': [
                {
                    'produto': item.produto,
                    'quantidade': item.quantidade,
                    'estampa': item.estampa,
                    'tamanho': item.tamanho,
                    'total_item': item.quantidade * item.produto.preco
                }
                for item in itens_carrinho
            ],
            'total': sum(item.quantidade * item.produto.preco for item in itens_carrinho)
        }
        
        return render(request, 'produto/confirmacao_compra.html', context)
