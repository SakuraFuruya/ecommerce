class CarritoDAO:
    @staticmethod
    def obtener(request):
        """Devuelve el carrito guardado en sesión."""
        return request.session.setdefault('carrito', {})

    @staticmethod
    def agregar(request, producto_id, cantidad=1):
        """Agrega un producto al carrito en sesión."""
        carrito = CarritoDAO.obtener(request)
        carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + cantidad
        request.session['carrito'] = carrito
        request.session.modified = True
        return carrito

    @staticmethod
    def eliminar(request, producto_id):
        """Elimina un producto del carrito en sesión."""
        carrito = CarritoDAO.obtener(request)
        carrito.pop(str(producto_id), None)
        request.session['carrito'] = carrito
        request.session.modified = True
        return carrito

    @staticmethod
    def limpiar(request):
        """Vacía el carrito en sesión."""
        request.session['carrito'] = {}
        request.session.modified = True
        return request.session['carrito']

    @staticmethod
    def obtener_productos(request):
        """Devuelve los productos del carrito como diccionario."""
        return CarritoDAO.obtener(request)


# Compatibilidad con el código anterior

def obtener_carrito_por_usuario(usuario):
    return None


def agregar_producto_al_carrito(usuario, producto_id, cantidad=1):
    return None


def eliminar_producto_del_carrito(usuario, producto_id):
    return None


def obtener_productos_del_carrito(usuario):
    return []
