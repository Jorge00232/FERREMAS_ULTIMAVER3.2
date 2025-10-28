import pytest
from django.test import TestCase
from django.urls import reverse
from ferreteria.models import Producto, Categoria, Subcategoria

@pytest.mark.django_db
class TestProductos(TestCase):
    
    def test_vista_catalogo(self, client):
        """Acceso al catálogo de productos"""
        response = client.get(reverse('catalogo'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/catalogo.html')
    
    def test_vista_producto_detalle(self, client, producto_test):
        """Visualización de detalles de producto"""
        response = client.get(reverse('producto_detalle', args=[producto_test.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/producto_detalle.html')
        self.assertContains(response, producto_test.nombre)
    
    def test_vista_subcategoria(self, client, subcategoria_test):
        """Productos por subcategoría"""
        response = client.get(reverse('subcategoria_productos', args=[subcategoria_test.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/subcategoria_productos.html')
    
    def test_producto_inexistente(self, client):
        """Búsqueda de producto inexistente"""
        response = client.get(reverse('producto_detalle', args=[999]))  # ID que no existe
        self.assertEqual(response.status_code, 404)
    
    def test_generacion_codigo_producto(self, subcategoria_test, marca_test):
        """Verificar que se genera código de producto automáticamente"""
        producto = Producto.objects.create(
            nombre='Destornillador',
            descripcion='Destornillador profesional',
            precio=8000,
            stock=5,
            subcategoria=subcategoria_test,
            marca=marca_test
        )
        
        self.assertTrue(producto.codigo_producto.startswith('FER-'))
        self.assertEqual(len(producto.codigo_producto), 9)  # FER-XXXXX