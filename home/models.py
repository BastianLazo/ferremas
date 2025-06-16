from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    descuento = models.PositiveIntegerField(default=0) 

    def precio_final(self):
        return self.precio * (1 - (self.descuento / 100))

    def __str__(self):
        return self.nombre


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='pendiente')
    archivo_boleta = models.FileField(upload_to='boletas/', null=True, blank=True)  # <--- NUEVO CAMPO

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"
    
class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario


class CodigoDescuento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Ej: 10 para 10%")
    activo = models.BooleanField(default=True)
    fecha_expiracion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} ({self.descuento_porcentaje}%)"


class SolicitudProducto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='solicitudes/', null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    rechazado = models.BooleanField(default=False)
    motivo_rechazo = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Solicitud: {self.nombre} (por {self.creado_por.username})"
    


    