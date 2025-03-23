from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from carrinho.models import Carrinho, ItemCarrinho
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from principal.decorators import group_required
from .models import *
from .forms import *


@login_required
def detalhes_produto(request, id):
    """
    Mostra os detalhes de um produto.
    
    :param id: identificador do produto
    :return: uma renderização da página de detalhes do produto
    """
    produto = Produto.objects.filter(id=id).first()
    
    if not produto:
        return redirect('listar_produtos')
    
    return render(request, 'produto/produto.html', {'produto': produto})


@login_required
@group_required('Administradores')
def listar_produtos(request):
    """
    Mostra uma lista de todos os produtos cadastrados no sistema.
    
    Requer permissão de Administrador.
    
    :param request: Requisição do usuário.
    :return: Uma renderização da página de listagem de produtos.
    """
    produtos = Produto.objects.all()
    
    return render(request, 'produto/listar_produtos.html', {'produtos': produtos})


@login_required
@group_required('Administradores')
def listar_tipos_produtos(request):
    """
    Mostra uma lista de todos os tipos de produtos cadastrados no sistema.
    
    Requer permissão de Administrador.
    
    :param request: Requisição do usuário.
    :return: Uma renderização da página de listagem de tipos de produtos.
    """
    form_tipo = CategoriaProdutoForm()
    tipos_produtos = CategoriaProduto.objects.all()
    
    return render(request, 'produto/listar_tipos_produtos.html', {"tipo_produto_form": form_tipo, "tipos_produtos": tipos_produtos})


@login_required
@group_required('Administradores')
def create_produto(request):
    """
    Cria um novo produto.
    
    Requer permissão de Administrador.
    
    :param request: Requisição do usuário.
    :return: Redireciona para a página de listagem de produtos.
    """
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
        else:
            return render(request, "form.html", {"form" : form, 'titulo': 'Criar produto'})
    else:
        form = ProdutoForm()
        return render(request, "form.html", {"form" : form, 'titulo': 'Criar produto'})
    

@login_required
@group_required('Administradores')
def edit_produto(request, id):
    """
    Edita um produto existente.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :param id: Id do produto a ser editado.
    :return: Redireciona para a página de listagem de produtos.
    """
    produto = Produto.objects.get(pk = id)
    print(produto)

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)

        if form.is_valid():
            form.save()

            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    context = {'form' : form, 'titulo' : 'Editar produto'}
    
    if produto.imagem and hasattr(produto.imagem, 'url'):
        context['current_image_url'] = produto.imagem.url
    
    return render(request, 'form.html', context)
    

@login_required
@group_required('Administradores')
def remove_produto(request, id):
    """
    Remove um produto existente.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :param id: Id do produto a ser deletado.
    :return: Redireciona para a página de listagem de produtos.
    """
    produto = Produto.objects.filter(pk = id)
    
    if produto: produto.delete()

    return redirect('listar_produtos')


@login_required
@group_required('Administradores')
def create_tipo_produto(request):
    """
    Cria um novo tipo de produto.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :return: Redireciona para a página de listagem de tipos de produtos.
    """
    if request.method == "POST":
        form = CategoriaProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_tipo_produtos")
        else:
            return redirect("listar_tipo_produtos")
    else:
        form = CategoriaProdutoForm()
        return redirect("listar_tipo_produtos")
    

@login_required
@group_required('Administradores')
def edit_tipo_produto(request, id):
    """
    Edita um tipo de produto pelo id.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :param id: Id do tipo de produto a ser editado.
    :return: Redireciona para a página de listagem de tipos de produtos.
    """
    categoriaProduto = CategoriaProduto.objects.get(pk = id)
    print(categoriaProduto)

    if request.method == "POST":
        form = CategoriaProdutoForm(request.POST, instance=categoriaProduto)

        if form.is_valid():
            form.save()
            
            return redirect('listar_tipo_produtos')
    else:
        form = CategoriaProdutoForm(instance=categoriaProduto)

    return render(request, "form.html", {'form' : form, 'titulo': 'Editar tipo de produto'})


@login_required
@group_required('Administradores')
def remove_tipo_produto(request, id):
    """
    Remove um tipo de produto pelo id.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :param id: Id do tipo de produto a ser removido.
    :return: Redireciona para a página de listagem de tipos de produtos.
    """
    categoriaProduto = CategoriaProduto.objects.filter(pk = id).first()
    
    if categoriaProduto: categoriaProduto.delete()

    return redirect('listar_tipo_produtos')


def pesquisar_produtos(request):
    """
    Mostra a lista de produtos filtrados por nome, descriço, categoria, preco, tamanho e ordenados por preco.
    
    :param request: Requisição do usuário.
    :return: Retorna a página de listagem de produtos.
    """
    produtos = Produto.objects.all()
    
    # Filtros
    pesquisa = request.GET.get('pesquisa', '').strip()
    categoria_id = request.GET.get('categoria')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    tamanho_id = request.GET.get('tamanho')
    sort = request.GET.get('sort', '')
    
    if sort == 'preco_asc':
        produtos = produtos.order_by('preco')
    elif sort == 'preco_desc':
        produtos = produtos.order_by('-preco')
        
    if pesquisa:
        produtos = produtos.filter(Q(nome__icontains=pesquisa) | Q(descricao__icontains=pesquisa))
        
    if categoria_id:
        produtos = produtos.filter(categorias__id=categoria_id)
    
    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)
    
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)
    
    if tamanho_id:
        produtos = produtos.filter(tamanho__id=tamanho_id)
    
    # Paginação
    paginator = Paginator(produtos, 12)  # Mostra 10 produtos por página
    page = request.GET.get('page')
    
    try:
        produtos_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exiba a primeira página.
        produtos_pagina = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (por exemplo, 9999), exiba a última página de resultados.
        produtos_pagina = paginator.page(paginator.num_pages)
    
    categorias = CategoriaProduto.objects.all()
    tamanhos = Tamanho.objects.all()
    
    context = {
        'produtos': produtos_pagina,
        'categorias': categorias,
        'tamanhos': tamanhos,
        'pesquisa': pesquisa,
        'preco_min': preco_min,
        'preco_max': preco_max,
        'categoria_id': int(categoria_id if categoria_id else 0),
        'tamanho_id': int(tamanho_id if tamanho_id else 0),
        'sort': sort,
    }
    return render(request, 'produto/pesquisa.html', context)


@login_required
def adicionar_ao_carrinho(request, id):
    """
    Adiciona um produto ao carrinho do usuário.

    Se o produto já estiver no carrinho, soma a quantidade desejada à quantidade atual.
    Se o produto não estiver no carrinho, adiciona-o com a quantidade desejada.

    :param request: Requisição do usuário.
    :param id: ID do produto a ser adicionado.
    :return: Redireciona para a página do carrinho.
    """
    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=id)
        usuario = request.user
        carrinho, created = Carrinho.objects.get_or_create(usuario=usuario)
        
        quantidade = int(request.POST.get('quantidade'))
        estampa_id = request.POST.get('estampa')
        tamanho_id = request.POST.get('tamanho')
        
        estampa = None
        tamanho = None
        
        if estampa_id is not None:
            estampa_id = int(estampa_id)
            estampa = get_object_or_404(Estampa, id=estampa_id)
            
        if tamanho_id is not None:
            tamanho_id = int(tamanho_id)
            tamanho = get_object_or_404(Tamanho, id=tamanho_id)
        
        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho, 
            produto=produto, 
            estampa=estampa, 
            tamanho=tamanho, 
            defaults={'quantidade': quantidade}
        )

        if not created:
            item.quantidade += quantidade
            item.save()

    return redirect('carrinho')


@login_required
def remover_do_carrinho(request, id):
    """
    Remove um produto do carrinho do usuário.

    :param id: ID do produto a ser removido.
    :return: Redireciona para a página do carrinho.
    """
    produto = get_object_or_404(Produto, id=id)
    usuario = request.user
    carrinho, created = Carrinho.objects.get_or_create(usuario=usuario)

    item_carrinho, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    
    if item_carrinho:
        item_carrinho.delete()

    return redirect('carrinho')