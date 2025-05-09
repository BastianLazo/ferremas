from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=30)
    last_name = forms.CharField(label='Apellido', max_length=30)
    email = forms.EmailField(label='Correo electrónico')
    rut = forms.CharField(label='RUT', max_length=12)
    address = forms.CharField(label='Dirección', max_length=255)
    phone = forms.CharField(label='Teléfono', max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'rut', 'address', 'phone', 'password1', 'password2')
