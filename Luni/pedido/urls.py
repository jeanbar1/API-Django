from django.urls import include, path
from . import views
from rest_framework import routers
from .views import ItemPedidoViewSet, PedidoViewSet

router = routers.DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'itenspedidos', ItemPedidoViewSet)

urlpatterns = [
    path('<int:id>/', views.pedido, name='pedido'), # detalhes do pedido
    path('listar_pedidos/', views.listar_pedidos, name='listar_pedidos'), # lista de pedidos
    path('listar_pedidos/<int:id>/', views.listar_pedidos, name='listar_pedidos'), # lista de pedidos de um cliente
    path('create/', views.create_pedido, name='create_pedido'), # cria um novo pedido
    path('update/<int:id>/', views.edit_pedido, name='edit_pedido'), # edita um pedido
    path('delete/<int:id>/', views.remove_pedido, name='delete_pedido'), # deleta um pedido

    # api routes
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),

]