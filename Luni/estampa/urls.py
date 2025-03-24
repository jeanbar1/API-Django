from django.urls import include, path
from . import views

from rest_framework.routers import DefaultRouter
from .views import EstampaViewSet

router = DefaultRouter()
router.register(r'estampas', EstampaViewSet)

urlpatterns = [
    path('listar_estampas/', views.listar_estampas, name='listar_estampas'), # lista de estampas
    path('create/', views.create_estampa, name='create_estampa'), # cria uma nova estampa
    path('update/<int:id>/', views.edit_estampa, name='edit_estampa'), # edita uma estampa
    path('delete/<int:id>/', views.remove_estampa, name='delete_estampa'), # remove uma estampa

    # routes api
    path('', include(router.urls)),
]