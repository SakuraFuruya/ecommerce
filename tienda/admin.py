import csv
import io
from decimal import Decimal, InvalidOperation

from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .models import Usuario, Producto, Pedido, Carrito

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    list_filter = ('precio', 'stock')
    search_fields = ('nombre', 'descripcion')
    change_list_template = 'admin/tienda/producto/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'importar-csv/',
                self.admin_site.admin_view(self.importar_csv),
                name='tienda_producto_importar_csv',
            ),
        ]
        return custom_urls + urls

    def importar_csv(self, request):
        if request.method == 'POST':
            archivo = request.FILES.get('archivo_csv')
            if not archivo:
                messages.error(request, 'Selecciona un archivo CSV.')
            else:
                try:
                    contenido = archivo.read().decode('utf-8-sig')
                    lector = csv.DictReader(io.StringIO(contenido))
                    columnas_requeridas = {'nombre', 'descripcion', 'precio', 'stock'}

                    if not lector.fieldnames or not columnas_requeridas.issubset(lector.fieldnames):
                        raise ValueError(
                            'El CSV debe tener las columnas: nombre, descripcion, precio y stock.'
                        )

                    productos_importados = 0
                    with transaction.atomic():
                        for numero_fila, fila in enumerate(lector, start=2):
                            nombre = fila['nombre'].strip()
                            if not nombre:
                                raise ValueError(f'La fila {numero_fila} no tiene nombre.')

                            try:
                                precio = Decimal(fila['precio'].strip())
                                stock = int(fila['stock'].strip())
                            except (InvalidOperation, TypeError, ValueError) as error:
                                raise ValueError(
                                    f'Precio o stock inválido en la fila {numero_fila}.'
                                ) from error

                            if precio < 0 or stock < 0:
                                raise ValueError(
                                    f'Precio o stock no puede ser negativo en la fila {numero_fila}.'
                                )

                            Producto.objects.update_or_create(
                                nombre=nombre,
                                defaults={
                                    'descripcion': fila['descripcion'].strip(),
                                    'precio': precio,
                                    'stock': stock,
                                },
                            )
                            productos_importados += 1

                    messages.success(
                        request,
                        f'Se importaron {productos_importados} productos correctamente.',
                    )
                    return HttpResponseRedirect(
                        reverse('admin:tienda_producto_changelist')
                    )
                except (UnicodeDecodeError, ValueError) as error:
                    messages.error(request, str(error))

        context = {
            **self.admin_site.each_context(request),
            'title': 'Importar productos desde CSV',
            'opts': self.model._meta,
        }
        return render(request, 'admin/tienda/producto/importar_csv.html', context)

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
