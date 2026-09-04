from django.contrib.auth import authenticate, get_user_model

Usuario = get_user_model()


class UsuarioDAO:
    @staticmethod
    def crear_usuario(username, email, password):
        """Crea un usuario nuevo usando el modelo custom de Django."""
        if Usuario.objects.filter(username=username).exists():
            raise ValueError('El usuario ya existe.')
        return Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

    @staticmethod
    def obtener_por_username(username):
        """Obtiene un usuario por su nombre de usuario."""
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def autenticar_usuario(username, password):
        """Autentica al usuario usando el backend default."""
        return authenticate(username=username, password=password)

    @staticmethod
    def eliminar_usuario(username):
        """Elimina un usuario por su username."""
        usuario = UsuarioDAO.obtener_por_username(username)
        if usuario:
            usuario.delete()
            return True
        return False


# Compatibilidad con el código anterior

def crear_usuario(username, email, password):
    return UsuarioDAO.crear_usuario(username, email, password)


def obtener_usuario_por_username(username):
    return UsuarioDAO.obtener_por_username(username)


def autenticar_usuario(username, password):
    return UsuarioDAO.autenticar_usuario(username, password)


def eliminar_usuario(username):
    return UsuarioDAO.eliminar_usuario(username)
