from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, UserProfile, Compra
from .cart import Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
import mercadopago
from django.conf import settings
import requests
from django.contrib import messages
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def homepage(request):
    return render(request, 'home/index.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'home/productos.html', {'productos': productos})


from .cart import Cart  

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except ValueError:
            cantidad = 1
    else:
        cantidad = 1

    cart.add(producto, cantidad)
    return redirect('ver_carrito')



def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.remove(producto.id)  
    return redirect('ver_carrito')


def ver_carrito(request):
    cart = Cart(request)
    return render(request, 'home/carrito.html', {'cart': cart})


def pago_exitoso(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'pago_exitoso.html')

def incrementar_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.add(producto, 1)  
    return redirect('ver_carrito')

def decrementar_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.subtract(producto)
    return redirect('ver_carrito')

def contacto(request):
    return render(request, 'home/contacto.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('index') 
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Crear perfil
            profile = UserProfile.objects.create(
                user=user,
                rut=form.cleaned_data['rut'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone']
            )

            login(request, user)
            return redirect('homepage')

    else:
        form = CustomUserCreationForm()
    return render(request, 'home/register.html', {'form': form})

def custom_logout_view(request):
    logout(request)
    return redirect('homepage')

from django.views.decorators.http import require_POST

def pagar_mercadopago(request):
    cart = Cart(request)
    total = cart.get_total()

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": "Compra en FERREMAS",
                "quantity": 1,
                "unit_price": float(total),
            }
        ],
        "back_urls": {
            "success": "https://www.google.com",  
            "failure": "https://www.google.com",
            "pending": "https://www.google.com",
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    print("Respuesta MercadoPago:", preference_response)

    if "init_point" in preference_response["response"]:
        init_point = preference_response["response"]["init_point"]
        return redirect(init_point)
    else:
        return render(request, "home/error_pago.html", {
            "error": preference_response["response"]
        })


def contacto(request):
    if request.method == 'POST':
        numero = "56992249556"  # Número completo con código de país (Chile)

        data = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                }
            }
        }

        headers = {
            "Authorization": f"Bearer {settings.META_WA_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://graph.facebook.com/v22.0/641826565684472/messages",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            messages.success(request, "Mensaje enviado exitosamente por WhatsApp.")
        else:
            messages.error(request, f"Error al enviar mensaje: {response.status_code} - {response.text}")

        return redirect('contacto')

    return render(request, 'home/contacto.html')


def olvide_contrasena(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            return redirect('restablecer_contrasena', username=user.username)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
    return render(request, 'home/olvide_contrasena.html')


def restablecer_contrasena(request, username):
    if request.method == 'POST':
        nueva_contra = request.POST.get('password')
        confirmar_contra = request.POST.get('confirm_password')
        if nueva_contra == confirmar_contra:
            try:
                user = User.objects.get(username=username)
                user.set_password(nueva_contra)
                user.save()
                messages.success(request, 'Contraseña restablecida exitosamente.')
                return redirect('login')  # ajusta si tu login tiene otro name
            except User.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    return render(request, 'home/restablecer_contrasena.html')

@login_required
def historial_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'home/historial_compras.html', {'compras': compras})