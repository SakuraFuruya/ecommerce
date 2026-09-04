from tienda.models import Pedido, PedidoProducto, Producto


class PedidoDAO:
    @staticmethod
    def crear_pedido(usuario, direccion, carrito, total):
        """Crea un pedido a partir del carrito en sesión."""
        if not carrito:
            raise ValueError('El carrito está vacío.')

        pedido = Pedido.objects.create(
            usuario=usuario,
            direccion=direccion,
            estado='pendiente',
            precio_total=total,
        )

        for producto_id, cantidad in carrito.items():
            producto = Producto.objects.get(id=producto_id)
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
            )

        return pedido

    @staticmethod
    def obtener_pedido_por_id(pedido_id):
        """Obtiene un pedido por su ID."""
        try:
            return Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return None

    @staticmethod
    def obtener_pedidos_por_usuario(usuario):
        """Devuelve todos los pedidos de un usuario."""
        return Pedido.objects.filter(usuario=usuario)

    @staticmethod
    def cancelar_pedido(pedido_id):
        """Cancela un pedido existente."""
        pedido = PedidoDAO.obtener_pedido_por_id(pedido_id)
        if pedido:
            pedido.delete()
            return True
        return False


# Compatibilidad con el código anterior

def crear_pedido(usuario, direccion=None, carrito=None, total=0):
    if carrito is None:
        carrito = {}
    if direccion is None:
        raise ValueError('Se requiere una dirección para crear el pedido.')
    return PedidoDAO.crear_pedido(usuario, direccion, carrito, total)


def obtener_pedido_por_id(pedido_id):
    return PedidoDAO.obtener_pedido_por_id(pedido_id)


def obtener_pedidos_por_usuario(usuario):
    return PedidoDAO.obtener_pedidos_por_usuario(usuario)


def cancelar_pedido(pedido_id):
    return PedidoDAO.cancelar_pedido(pedido_id)
