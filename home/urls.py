# home/urls.py
from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .views import register_view, pagar_mercadopago  

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('productos/', views.productos, name='productos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('carrito/pagar/', views.pagar_mercadopago, name='pagar_mercadopago'),

    path('carrito/incrementar/<int:producto_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('carrito/decrementar/<int:producto_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('contacto/', views.contacto, name='contacto'),
    path('registro/', register_view, name='registro'),
    path('login/', LoginView.as_view(template_name='home/login.html',success_url=reverse_lazy('homepage')), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('carrito/pagar/', views.pagar_mercadopago, name='pagar'),

    path('pagar-mercado/', views.pagar_mercadopago, name='pagar_mercado'),





]
