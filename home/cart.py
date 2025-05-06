class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            self.cart[producto_id]['cantidad'] += cantidad
        else:
            self.cart[producto_id] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad,
                'imagen': producto.imagen.url if producto.imagen else ''
            }
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, producto_id):
        producto_id = str(producto_id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def subtract(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            if self.cart[producto_id]['cantidad'] > 1:
                self.cart[producto_id]['cantidad'] -= 1
            else:
                del self.cart[producto_id]
            self.save()

    def get_items(self):
        items = []
        for key, item in self.cart.items():
            item['total'] = item['precio'] * item['cantidad']
            items.append((key, item))
        return items

    def get_total(self):
        total = 0
        for item in self.cart.values():
            total += item['precio'] * item['cantidad']
        return int(total)
