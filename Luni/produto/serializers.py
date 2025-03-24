from rest_framework import serializers
from .models import CategoriaProduto, Tamanho, Produto
from estampa.models import Estampa  # Importe o modelo Estampa se necessário

class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = ['id', 'nome']

class TamanhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamanho
        fields = ['id', 'tamanho']

class ProdutoSerializer(serializers.ModelSerializer):
    # Relacionamentos ManyToMany representados por IDs primários
    categorias = serializers.PrimaryKeyRelatedField(
        queryset=CategoriaProduto.objects.all(),
        many=True
    )
    tamanho = serializers.PrimaryKeyRelatedField(
        queryset=Tamanho.objects.all(),
        many=True,
        required=False
    )
    estampas = serializers.PrimaryKeyRelatedField(
        queryset=Estampa.objects.all(),
        many=True,
        required=False
    )
    
    # Campo de imagem para upload
    imagem = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,
        use_url=True,
        required=False
    )

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'descricao', 'categorias', 
            'preco', 'tamanho', 'quantidade_em_estoque', 
            'estampas', 'imagem'
        ]