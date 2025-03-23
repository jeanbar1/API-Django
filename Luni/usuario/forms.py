from django import forms
from django.contrib.auth.forms import SetPasswordMixin
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagem', 'username', 'email', 'telefone', 'endereco', 'cpf']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o e-mail'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    
class UsuarioFormSingup(forms.ModelForm):
    password1, password2 = SetPasswordMixin.create_password_fields()
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefone', 'endereco', 'cpf',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o e-mail'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CPF'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a senha'}),
        }

        