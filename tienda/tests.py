from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Pedido, Producto


class TiendaFlowTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Laptop X',
            descripcion='Portátil ligera',
            precio=999.99,
            stock=5,
        )
        self.user = get_user_model().objects.create_user(
            username='cliente1',
            password='12345678',
        )

    def test_catalogo_muestra_productos(self):
        response = self.client.get(reverse('lista_productos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop X')

    def test_checkout_requires_login(self):
        self.client.session['carrito'] = {str(self.producto.id): 1}
        self.client.session.save()

        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_checkout_crea_pedido_con_usuario_autenticado(self):
        self.client.force_login(self.user)
        session = self.client.session
        session['carrito'] = {str(self.producto.id): 2}
        session.save()

        response = self.client.post(
            reverse('checkout'),
            {'direccion': 'Calle Falsa 123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Pedido.objects.filter(usuario=self.user).exists())
