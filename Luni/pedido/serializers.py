from .models import Pedido, ItemPedido
from rest_framework import serializers

# Serializers define the API representation.
class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):     
    class Meta:
        model = Pedido
        fields = '__all__'
