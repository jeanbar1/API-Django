from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Usuario

#import para o token:
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate




class UsuarioSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    qnt_itens = serializers.SerializerMethodField()
    imagem = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'telefone', 'endereco',
            'tipo_cliente', 'cpf', 'imagem', 'is_superuser',
            'groups', 'qnt_itens'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_qnt_itens(self, obj):
        return obj.get_size_items()

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request', None)
        
        if request and not request.user.is_superuser:
            fields['tipo_cliente'].read_only = True
            fields['is_superuser'].read_only = True
        return fields

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'telefone',
            'endereco', 'cpf', 'password', 'password2', 'imagem'
        ]
        extra_kwargs = {
            'imagem': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "As senhas não coincidem."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        validated_data['tipo_cliente'] = 'CLIENTE'
        
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        
        grupo = Group.objects.get_or_create(name='Clientes')[0]
        user.groups.add(grupo)
        
        return user

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'telefone',
            'endereco', 'cpf', 'imagem'
        ]
        extra_kwargs = {
            'imagem': {'required': False, 'allow_null': True},
        }

class MudarTipoUsuarioSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(choices=Usuario.TIPOS_CLIENTE)

    def update(self, instance, validated_data):
        tipo = validated_data.get('tipo')
        instance.tipo_cliente = tipo
        instance.groups.clear()

        grupo_map = {
            'CLIENTE': 'Clientes',
            'ADMINISTRADOR': 'Administradores',
            'CORPORATIVO': 'Corporativos'
        }

        grupo_nome = grupo_map.get(tipo, 'Clientes')
        grupo, _ = Group.objects.get_or_create(name=grupo_nome)
        
        instance.groups.add(grupo)
        instance.is_superuser = (tipo == 'ADMINISTRADOR')
        instance.save()
        
        return instance
    
    #class para criação do token
    
    class TokenObtainPairSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)
        def validate(self, attrs):
            username = attrs.get('username')
            password = attrs.get('password')

            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Credenciais inválidas.")

            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }