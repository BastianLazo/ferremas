from django.shortcuts import render
from .models import Producto  # Asegúrate de importar tu modelo

def homepage(request):
    return render(request, 'home/index.html')

def productos(request):
    productos = Producto.objects.all()  # Trae todos los productos de la base de datos
    return render(request, 'home/productos.html', {'productos': productos})
