# home/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view, pagar_mercadopago, CustomLoginView, admin_home
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

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
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('carrito/pagar/', views.pagar_mercadopago, name='pagar'),
    path('pagar-mercado/', views.pagar_mercadopago, name='pagar_mercado'),
    path('olvide-contrasena/', auth_views.PasswordResetView.as_view(template_name='home/olvide_contrasena.html'), name='password_reset'),
    path('olvide-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    path('restablecer-contrasena/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/restablecer_contrasena.html'), name='password_reset_confirm'),
    path('restablecer-contrasena/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),
    path('historial/', views.historial_compras, name='historial_compras'),
    path('admin-home/', admin_home, name='admin_home'),
    path('admin-ferremas/productos/', views.listar_productos_admin, name='listar_productos_admin'),
    path('admin-ferremas/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('admin-ferremas/productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('admin-ferremas/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('bodega/', views.bodeguero_home, name='bodeguero_home'),
    path('bodega/productos/', views.listar_productos_bodeguero, name='listar_productos_bodeguero'),
    path('bodega/productos/editar/<int:producto_id>/', views.editar_stock_bodeguero, name='editar_stock_bodeguero'),
    path('bodega/productos/agregar/', views.agregar_producto_bodeguero, name='agregar_producto_bodeguero'),
    path('bodega/solicitar-agregar/', views.solicitar_agregar_producto, name='solicitar_agregar_producto'),
    path('admin/solicitudes/', views.revisar_solicitudes, name='revisar_solicitudes'),
    path('admin/solicitudes/aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('bodega/mis-solicitudes/', views.ver_solicitudes_bodeguero, name='ver_solicitudes_bodeguero'),
    path('panel/solicitudes/', views.revisar_solicitudes, name='revisar_solicitudes'),
    path('panel/solicitudes/aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('panel/solicitudes/rechazar/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),





]
