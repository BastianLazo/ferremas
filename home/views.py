
from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'home/index.html')

def productos(request):
    productos = [
        {'nombre': 'Martillo tradicional', 'precio': 3990, 'imagen': 'images/Martillo.png'},
        {'nombre': 'Atornillador electrico', 'precio': 4490, 'imagen': 'images/atornilladorelectrico.jpg'},
        {'nombre': 'Pintura de interior', 'precio': 2990, 'imagen': 'images/pinturainterior.jpg'},
    ]
    return render(request, 'home/productos.html', {'productos': productos})