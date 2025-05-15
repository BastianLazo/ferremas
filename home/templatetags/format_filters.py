from django import template

register = template.Library()

@register.filter
def punto_miles(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except:
        return value


@register.filter
def precio_con_descuento(producto):
    try:
        descuento = float(producto.descuento)
        precio = float(producto.precio)
        if descuento > 0:
            precio_final = precio * (1 - descuento / 100)
            return f"{precio_final:,.0f}".replace(",", ".")  
        return f"{precio:,.0f}".replace(",", ".")
    except: 
        return producto.precio
    
   