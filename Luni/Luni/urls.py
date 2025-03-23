from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


def error_handler(request, exception=None, status_code=None):

    """
    Tratador de erros genérico para o Django.

    Esta view recebe um request, um exception e um status_code como parâmetros.
    Se o status_code n o for informado, ele padroniza-se como 500.
    A view retorna um HttpResponse com o status code informado e um template
    chamado 'error.html' com dois par metros: status_code e exception.
    O template 'error.html' é responsável por exibir uma página de erro amigável
    ao usuário.

    :param request: O request atual.
    :type request: django.http.HttpRequest
    :param exception: O exception que ocorreu.
    :type exception: Exception
    :param status_code: O status code que será retornado.
    :type status_code: int
    """
    if status_code is None:
        status_code = 500
    context = {
        'status_code': status_code,
        'exception': exception,
    }
    return render(request, 'error.html', context, status=status_code)


handler400 = error_handler
handler403 = error_handler
handler404 = error_handler
handler500 = error_handler


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("principal.urls"), name="index"),
    path("user/", include("usuario.urls"), name='usuario'),
    path("produto/", include("produto.urls"), name='produto'),
    path("estampa/", include("estampa.urls"), name='estampa'),
    path("carrinho/", include("carrinho.urls"), name='carrinho'),
    path("pedido/", include("pedido.urls"), name='pedido'),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)