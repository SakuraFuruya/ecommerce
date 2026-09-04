from django.contrib import admin
from .models import Usuario, Producto, Pedido, Carrito

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    list_filter = ('precio', 'stock')
    search_fields = ('nombre', 'descripcion')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_pedido', 'estado', 'precio_total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__username', 'direccion')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'subtotal')
    list_filter = ('usuario',)
    search_fields = ('usuario__username', 'producto__nombre')

admin.site.site_header = "Administración E-commerce"
admin.site.site_title = "Panel de Control E-commerce"
admin.site.index_title = "Bienvenido al Panel de Administración"
