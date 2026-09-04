from tienda.models import Producto


class ProductoDAO:
    @staticmethod
    def listar_productos():
        """Devuelve todos los productos."""
        return Producto.objects.all()

    @staticmethod
    def obtener_producto(producto_id):
        """Devuelve un producto por su ID."""
        return Producto.objects.get(id=producto_id)

    @staticmethod
    def buscar_por_nombre(nombre):
        """Busca productos por coincidencia parcial en el nombre."""
        return Producto.objects.filter(nombre__icontains=nombre)


# Compatibilidad con el código anterior

def listar_productos():
    return ProductoDAO.listar_productos()


def obtener_producto(producto_id):
    return ProductoDAO.obtener_producto(producto_id)


def buscar_productos_por_nombre(nombre):
    return ProductoDAO.buscar_por_nombre(nombre)
