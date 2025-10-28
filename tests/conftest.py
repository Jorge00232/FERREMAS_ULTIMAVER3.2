import pytest
from django.contrib.auth.models import User
from ferreteria.models import Producto, Categoria, Subcategoria, CarritoItem, Order, Marca

@pytest.fixture
def usuario_test():
    """Fixture para crear un usuario de prueba"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def categoria_test():
    """Fixture para crear una categoría de prueba"""
    return Categoria.objects.create(nombre='Herramientas')

@pytest.fixture
def subcategoria_test(categoria_test):
    """Fixture para crear una subcategoría de prueba"""
    return Subcategoria.objects.create(
        nombre='Martillos',
        categoria=categoria_test
    )

@pytest.fixture
def marca_test():
    """Fixture para crear una marca de prueba"""
    return Marca.objects.create(nombre='Stanley')

@pytest.fixture
def producto_test(subcategoria_test, marca_test):
    """Fixture para crear un producto de prueba"""
    return Producto.objects.create(
        nombre='Martillo de Acero',
        descripcion='Martillo profesional de acero forjado',
        precio=15000,
        stock=10,
        subcategoria=subcategoria_test,
        marca=marca_test
    )

@pytest.fixture
def carrito_item_test(usuario_test, producto_test):
    """Fixture para crear un item de carrito de prueba"""
    return CarritoItem.objects.create(
        user=usuario_test,
        producto=producto_test,
        cantidad=2
    )

@pytest.fixture
def order_test(usuario_test):
    """Fixture para crear una orden de prueba"""
    return Order.objects.create(
        user=usuario_test,
        total_amount=30000,
        delivery_method='pickup'
    )

@pytest.fixture
def cliente_autenticado(client, usuario_test):
    """Fixture para cliente autenticado"""
    client.force_login(usuario_test)
    return client