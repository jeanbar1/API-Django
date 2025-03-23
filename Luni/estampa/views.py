from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from principal.decorators import group_required
from .models import *
from .forms import *

@group_required('Administradores')
@login_required
def listar_estampas(request):
    """
    Lista todas as estampas do banco de dados.

    Requer permiss o de Administrador.

    :param request: Requisição do usuário.
    :return: Retorna uma página HTML com a lista de estampas.
    """
    estampas = Estampa.objects.all()
    return render(request, 'estampa/listar_estampas.html', {'estampas': estampas})


@group_required('Administradores')
@login_required
def create_estampa(request):
    """
    Cria uma estampa.

    Requer permiss o de Administrador.

    :param request: Requisição do usuário.
    :return: Redireciona para a página de listagem de estampas.
    """
    if request.method == "POST":
        form = EstampaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/estampa/')
        else:
            return render(request, "form.html", {"form" : form, 'titulo' : 'Criar Estampa'})
    else:
        form = EstampaForm()
        return render(request, "form.html", {"form" : form, 'titulo' : 'Criar Estampa'})
    

@group_required('Administradores')
@login_required
def edit_estampa(request, id):
    """
    Edita uma estampa pelo id.

    Requer permissão de Administrador.

    :param request: Requisição do usuário.
    :param id: Id da estampa a ser editada.
    :return: Redireciona para a página de listagem de estampas.
    """
    estampa = Estampa.objects.get(pk = id)
    print(estampa)

    if request.method == "POST":
        form = EstampaForm(request.POST, request.FILES, instance=estampa)

        if form.is_valid():
            form.save()

            return redirect('/estampa/')
    else:
        form = EstampaForm(instance=estampa)

    context = {'form' : form, 'titulo' : 'Editar Estampa'}
    
    if estampa.imagem and hasattr(estampa.imagem, 'url'):
        context['current_image_url'] = estampa.imagem.url
    
    return render(request, 'form.html', context)


@group_required('Administradores')
@login_required
def remove_estampa(request, id):
    """
    Remove uma estampa pelo id.

    Requer permiss o de Administrador.

    :param request: Requisição do usuário.
    :param id: Id da estampa a ser removida.
    :return: Redireciona para a página de listagem de estampas.
    """
    estampa = Estampa.objects.filter(pk = id).first()
    
    if estampa: estampa.delete()
    
    return redirect('listar_estampas')