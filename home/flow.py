import requests
import hashlib

# Claves de Flow (reemplaza con las tuyas reales del panel)
API_KEY = '72E7C11F-CDFD-4C37-BE61-69D8D0LD2EA7'
SECRET_KEY = '0ca59d6d4630dd78ce7d9488fc7ae86cd9ad4c61'

# URL de la API de Flow en modo sandbox
FLOW_API_URL = 'https://sandbox.flow.cl/api/payment/create'

def crear_pago(cart, return_url):
    total = cart.get_total()
    
    # Construimos el mensaje de orden
    items = [f"{item['cantidad']} x {item['nombre']}" for _, item in cart.get_items()]
    descripcion = ", ".join(items)

    data = {
        "commerceOrder": "ORD" + hashlib.md5(descripcion.encode()).hexdigest()[:10],
        "subject": "Pago Ferremas",
        "currency": "CLP",
        "amount": str(total),
        "email": "cliente@demo.cl",  # Puedes poner uno real si gustas
        "urlConfirmation": return_url,
        "urlReturn": return_url,
        "paymentMethod": 9  # 9 = Webpay, puedes usar 1 para todos los métodos
    }

    # Firma del mensaje (ordenada según la documentación de Flow)
    cadena = f"{data['commerceOrder']}{data['subject']}{data['currency']}{data['amount']}{data['email']}{data['urlConfirmation']}{data['urlReturn']}{data['paymentMethod']}"
    firma = hashlib.sha256((cadena + SECRET_KEY).encode()).hexdigest()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Enviamos el POST con los datos y la firma
    response = requests.post(FLOW_API_URL, data={
        **data,
        "apiKey": API_KEY,
        "s": firma
    }, headers=headers)

    return response.json()
