from django.db import models
from django.contrib.auth.models import AbstractUser

# Extensión del modelo de usuario de Django
class Usuario(AbstractUser):
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[('cliente', 'Cliente'), ('admin', 'Administrador'), ('operador', 'Operador')],
        default='cliente'
    )

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.username}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="productos")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carrito"

    def __str__(self):
        return f"Carrito de {self.usuario.username} - {self.producto.nombre} x {self.cantidad}"
