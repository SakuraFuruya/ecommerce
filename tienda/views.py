from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Pedido, PedidoProducto, Producto, Usuario


def _get_carrito(request):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict):
        carrito = {}
    request.session['carrito'] = carrito
    request.session.modified = True
    return carrito


def _carrito_con_total(request):
    carrito = _get_carrito(request)
    items = []
    total = Decimal('0.00')

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, pk=producto_id)
        subtotal = producto.precio * cantidad
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio_unitario': producto.precio,
            'subtotal': subtotal,
        })
        total += subtotal

    return items, total


def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/inicio.html', {'productos': productos})


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/lista_productos.html', {'productos': productos})


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = _get_carrito(request)
    carrito = dict(carrito)
    carrito[str(producto.id)] = carrito.get(str(producto.id), 0) + 1
    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('lista_productos')


def ver_carrito(request):
    items, total = _carrito_con_total(request)
    return render(request, 'tienda/carrito.html', {
        'carrito_items': items,
        'total': total,
        'carrito_vacio': not items,
    })


def eliminar_del_carrito(request, producto_id):
    carrito = dict(_get_carrito(request))
    carrito.pop(str(producto_id), None)
    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('ver_carrito')


@login_required(login_url='login')
def checkout(request):
    carrito = dict(_get_carrito(request))
    if not carrito:
        return redirect('lista_productos')

    items, total = _carrito_con_total(request)

    if request.method == 'POST':
        direccion = (request.POST.get('direccion') or '').strip()
        if not direccion:
            return render(request, 'tienda/checkout.html', {
                'carrito_items': items,
                'total': total,
                'error': 'Debes ingresar una dirección de entrega.',
            })

        pedido = Pedido.objects.create(
            usuario=request.user,
            direccion=direccion,
            estado='pendiente',
            precio_total=0,
        )

        for producto_id, cantidad in carrito.items():
            producto = get_object_or_404(Producto, pk=producto_id)
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )

        pedido.precio_total = total
        pedido.save(update_fields=['precio_total'])
        request.session['carrito'] = {}
        request.session.modified = True

        return render(request, 'tienda/pedido_exitoso.html', {'pedido': pedido})

    return render(request, 'tienda/checkout.html', {
        'carrito_items': items,
        'total': total,
    })


def crear_pedido(request):
    return redirect('checkout')
