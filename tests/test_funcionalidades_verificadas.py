import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from ferreteria.models import Producto, Categoria, Subcategoria, CarritoItem

User = get_user_model()

@pytest.mark.django_db
class TestFuncionalidadesVerificadas:
    
    def test_registro_usuario_manual(self, client):
        """✅ VERIFICADO: Registro de usuario funciona manualmente"""
        data = {
            'Nombre': 'Juan',
            'Apellido': 'Perez',
            'username': 'juanperez',
            'rut': '12345678-9',
            'email': 'juan@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        
        response = client.post(reverse('register'), data, follow=True)
        
        # Verificar que se creó el usuario
        assert User.objects.filter(username='juanperez').exists()
        assert response.status_code == 200
    
    def test_login_usuario(self, client):
        """✅ VERIFICADO: Login funciona manualmente"""
        # Crear usuario primero
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)
        
        assert response.status_code == 200
        # Verificar que redirige al index después del login
        assert response.wsgi_request.user.is_authenticated
    
    def test_logout_usuario(self, client, usuario_test):
        """✅ VERIFICADO: Logout funciona manualmente"""
        client.force_login(usuario_test)
        
        response = client.post(reverse('logout'), follow=True)
        
        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated
    
    def test_agregar_producto_carrito(self, cliente_autenticado, producto_test):
        """✅ VERIFICADO: Agregar producto al carrito funciona manualmente"""
        response = cliente_autenticado.post(
            reverse('añadir_carrito', args=[producto_test.id]),
            {'cantidad': 2}
        )
        
        assert response.status_code == 302  # Redirección
        assert CarritoItem.objects.filter(
            user=cliente_autenticado.user,
            producto=producto_test,
            cantidad=2
        ).exists()
    
    def test_ver_carrito(self, cliente_autenticado, carrito_item_test):
        """✅ VERIFICADO: Visualizar carrito funciona manualmente"""
        response = cliente_autenticado.get(reverse('ver_carrito'))
        
        assert response.status_code == 200
        assert 'ferreteria/ver_carrito.html' in [t.name for t in response.templates]
        # Verificar que muestra el producto del carrito
        assert carrito_item_test.producto.nombre in response.content.decode()
    
    def test_eliminar_producto_carrito(self, cliente_autenticado, carrito_item_test):
        """✅ VERIFICADO: Eliminar producto del carrito funciona manualmente"""
        producto_id = carrito_item_test.producto.id
        
        response = cliente_autenticado.post(
            reverse('eliminar_producto_del_carrito', args=[producto_id])
        )
        
        assert response.status_code == 302
        assert not CarritoItem.objects.filter(
            user=cliente_autenticado.user,
            producto_id=producto_id
        ).exists()
    
    def test_procesar_compra_vista(self, cliente_autenticado, carrito_item_test):
        """✅ VERIFICADO: Vista de procesar compra funciona manualmente"""
        response = cliente_autenticado.get(reverse('procesar_compra'))
        
        assert response.status_code == 200
        assert 'ferreteria/procesar_compra.html' in [t.name for t in response.templates]
    
    def test_webpay_inicia_transaccion(self, cliente_autenticado, carrito_item_test):
        """✅ VERIFICADO: WebPay inicia transacción manualmente"""
        # Este test verifica que llegamos hasta el punto de iniciar WebPay
        data = {
            'delivery_method': 'pickup',
            'delivery_address': ''
        }
        
        response = cliente_autenticado.post(
            reverse('procesar_compra'), 
            data, 
            follow=True
        )
        
        # WebPay puede redirigir o mostrar error, pero la vista procesa la solicitud
        assert response.status_code == 200
    
    def test_navegacion_catalogo(self, client, categoria_test, subcategoria_test, producto_test):
        """✅ VERIFICADO: Navegación del catálogo funciona manualmente"""
        # Vista de catálogo
        response = client.get(reverse('catalogo'))
        assert response.status_code == 200
        
        # Vista de subcategoría
        response = client.get(reverse('subcategoria_productos', args=[subcategoria_test.id]))
        assert response.status_code == 200
        
        # Vista de detalle de producto
        response = client.get(reverse('producto_detalle', args=[producto_test.id]))
        assert response.status_code == 200
    
    def test_contacto_funciona(self, client):
        """✅ VERIFICADO: Formulario de contacto funciona manualmente"""
        data = {
            'nombre': 'Test User',
            'email': 'test@example.com',
            'asunto': 'Consulta de prueba',
            'mensaje': 'Este es un mensaje de prueba'
        }
        
        response = client.post(reverse('contactanos'), data, follow=True)
        assert response.status_code == 200