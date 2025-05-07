# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.productos, name='productos'),
     path('carrito/', views.ver_carrito, name='ver_carrito'),
   path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('carrito/pagar/', views.pagar, name='pagar'),
    path('pagar/', views.pagar, name='pagar'),
    path('carrito/incrementar/<int:producto_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('carrito/decrementar/<int:producto_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('contacto/', views.contacto, name='contacto'),

]
