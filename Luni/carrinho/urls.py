from django.urls import include, path
from . import views
from .views import CarrinhoViewSet, ItemCarrinhoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'carrinhos', CarrinhoViewSet)
router.register(r'itenscarrinhos', ItemCarrinhoViewSet)

urlpatterns = [
    path('', views.carrinho, name='carrinho'), # página do carrinho
    path('<int:id>', views.carrinho, name='carrinho'), # página do carrinho do usuário com o id
    path('atualizar_carrinho/', views.atualizar_carrinho, name='atualizar_carrinho'), # atualiza o carrinho
    path('confirmar_compra/', views.confirmar_compra, name='confirmar_compra'), # confirma a compra

    # api routes
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
