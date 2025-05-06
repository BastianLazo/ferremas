from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto  # Asegúrate de importar tu modelo
from .cart import Cart
from .flow import crear_pago

def homepage(request):
    return render(request, 'home/index.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'home/productos.html', {'productos': productos})


from .cart import Cart  # ajusta el path si es necesario

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
    cart.remove(producto.id)  # Aquí va solo el ID, no el objeto
    return redirect('ver_carrito')


def ver_carrito(request):
    cart = Cart(request)
    return render(request, 'home/carrito.html', {'cart': cart})



def pagar(request):
    cart = Cart(request)
    return_url = request.build_absolute_uri('/pago_exitoso/')
    pago = crear_pago(cart, return_url)

    if 'url' in pago:
        return redirect(pago['url'])
    else:
        return redirect('ver_carrito')
    
def pago_exitoso(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'pago_exitoso.html')

def incrementar_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.add(producto, 1)  # suma uno
    return redirect('ver_carrito')

def decrementar_cantidad(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cart = Cart(request)
    cart.subtract(producto)
    return redirect('ver_carrito')

