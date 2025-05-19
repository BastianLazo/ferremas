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
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.contrib.auth.decorators import user_passes_test
from .models import SolicitudProducto, Producto
from django.utils import timezone
from .models import CompraItem
from .models import Compra


def homepage(request):
    productos = Producto.objects.all()[:5]  
    return render(request, 'home/index.html', {'productos': productos})

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


@login_required
def pago_exitoso(request):
    cart = Cart(request)

    if not cart.cart:
        return redirect('homepage')  

    compra = Compra.objects.create(
        usuario=request.user,
        total=cart.get_total()
    )

    for key, item in cart.get_items():
        CompraItem.objects.create(
            compra=compra,
            producto_id=item['producto_id'],
            cantidad=item['cantidad'],
            precio_unitario=item['precio']
        )

    cart.clear()

    return render(request, 'home/pago_exitoso.html')



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

from django.urls import reverse

def pagar_mercadopago(request):
    cart = Cart(request)
    total = cart.get_total()

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    success_url = "https://19d2-186-78-253-73.ngrok-free.app/pago_exitoso/"


    preference_data = {
    "items": [
        {
            "title": "Compra en FERREMAS",
            "quantity": 1,
            "unit_price": float(total),
        }
    ],
    "back_urls": {
        "success": success_url,
        "failure": success_url,
        "pending": success_url,
    },
    "auto_return": "approved",
}


    preference_response = sdk.preference().create(preference_data)

    if "init_point" in preference_response["response"]:
        return redirect(preference_response["response"]["init_point"])
    else:
        return render(request, "home/error_pago.html", {
            "error": preference_response["response"]
        })


def contacto(request):
    if request.method == 'POST':
        numero = "56992249556"  

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

def historial_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'home/historial_compras.html', {'compras': compras})


class CustomLoginView(LoginView):
    template_name = 'home/login.html'

    def form_valid(self, form):
        """ Redirecciona según grupo una vez autenticado. """
        user = form.get_user()
        login(self.request, user)  # Asegura el login

        if user.is_superuser:
            return redirect('admin_home')
        elif user.groups.filter(name='Bodeguero').exists():
            return redirect('bodeguero_home')
        elif user.groups.filter(name='Vendedor').exists():
            return redirect('compras_pendientes_vendedor')
        return redirect('homepage')


@login_required
def admin_home(request):
    return render(request, 'home/admin_home.html')



from django.contrib.auth.decorators import user_passes_test


def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin)
def listar_productos_admin(request):
    productos = Producto.objects.all()
    return render(request, 'admin/productos_list.html', {'productos': productos})

@user_passes_test(es_admin)
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')
        stock = request.POST.get('stock')
        descuento = request.POST.get('descuento', 0)
        Producto.objects.create(nombre=nombre, descripcion=descripcion, precio=precio, imagen=imagen, stock=stock,descuento=descuento)
        return redirect('listar_productos_admin')
    return render(request, 'admin/producto_form.html')

@user_passes_test(es_admin)
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.descuento = request.POST.get('descuento', 0)

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('listar_productos_admin')

    return render(request, 'admin/producto_form.html', {'producto': producto})

@user_passes_test(es_admin)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('listar_productos_admin')

def es_vendedor(user):
    return user.groups.filter(name='Vendedor').exists()


def es_bodeguero(user):
    return user.groups.filter(name='Bodeguero').exists()

@user_passes_test(es_bodeguero)
def bodeguero_home(request):
    return render(request, 'bodega/bodeguero_home.html')

@user_passes_test(es_bodeguero)
def listar_productos_bodeguero(request):
    productos = Producto.objects.all()
    return render(request, 'bodega/productos_list.html', {'productos': productos})

@user_passes_test(es_bodeguero)
def editar_stock_bodeguero(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        nuevo_stock = request.POST.get('stock')
        if nuevo_stock.isdigit():
            producto.stock = int(nuevo_stock)
            producto.save()
            return redirect('listar_productos_bodeguero')

    return render(request, 'bodega/editar_stock.html', {'producto': producto})


@user_passes_test(es_bodeguero)
def agregar_producto_bodeguero(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=imagen
        )

        return redirect('listar_productos_bodeguero')

    return render(request, 'bodega/agregar_producto.html')



@user_passes_test(es_bodeguero)
def solicitar_agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')

        SolicitudProducto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=imagen,
            creado_por=request.user
        )

        messages.success(request, "Solicitud enviada al administrador.")
        return redirect('listar_productos_bodeguero')

    return render(request, 'bodega/solicitar_agregar_producto.html')


@user_passes_test(es_admin)
def revisar_solicitudes(request):
    solicitudes = SolicitudProducto.objects.filter(aprobado=False)
    return render(request, 'admin/solicitudes_pendientes.html', {'solicitudes': solicitudes})

@user_passes_test(es_admin)
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudProducto, id=solicitud_id)

  
    Producto.objects.create(
        nombre=solicitud.nombre,
        descripcion=solicitud.descripcion,
        precio=solicitud.precio,
        stock=solicitud.stock,
        imagen=solicitud.imagen
    )

    solicitud.aprobado = True
    solicitud.save()
    return redirect('revisar_solicitudes')


@user_passes_test(es_bodeguero)
def ver_solicitudes_bodeguero(request):
    solicitudes = SolicitudProducto.objects.filter(creado_por=request.user).order_by('-fecha_creacion')
    return render(request, 'bodega/mis_solicitudes.html', {'solicitudes': solicitudes})



@staff_member_required
def revisar_solicitudes(request):
    solicitudes = SolicitudProducto.objects.filter(aprobado=False, rechazado=False)
    return render(request, 'admin/solicitudes_pendientes.html', {'solicitudes': solicitudes})


@staff_member_required
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudProducto, id=solicitud_id)

    # Crear producto aprobado
    Producto.objects.create(
        nombre=solicitud.nombre,
        descripcion=solicitud.descripcion,
        precio=solicitud.precio,
        stock=solicitud.stock,
        imagen=solicitud.imagen
    )

    solicitud.aprobado = True
    solicitud.save()

    return redirect('revisar_solicitudes')


@staff_member_required
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudProducto, id=solicitud_id)

    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        solicitud.rechazado = True
        solicitud.motivo_rechazo = motivo
        solicitud.save()
        messages.success(request, "La solicitud ha sido rechazada.")
        return redirect('revisar_solicitudes')

    return render(request, 'admin/rechazar_solicitud.html', {'solicitud': solicitud})




@user_passes_test(es_vendedor)
def cambiar_estado_compra(request, compra_id, nuevo_estado):
    compra = get_object_or_404(Compra, id=compra_id)
    compra.estado = nuevo_estado
    compra.save()
    return redirect('compras_pendientes_vendedor')

def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group, login_url='login')


@user_passes_test(es_bodeguero)
def compras_pendientes_bodeguero(request):
    compras = Compra.objects.filter(estado='pendiente').order_by('-fecha')
    # Aquí puedes mostrar solo información de stock o preparar despacho
    return render(request, 'bodega/compras_pendientes.html', {'compras': compras})


@user_passes_test(es_vendedor)
def compras_pendientes_vendedor(request):
    compras = Compra.objects.filter(estado='pendiente').order_by('-fecha')
    return render(request, 'vendedor/compras_pendientes_vendedor.html', {'compras': compras})

