import pytest
from django.test import TestCase
from django.urls import reverse
from ferreteria.models import CarritoItem, Producto

@pytest.mark.django_db
class TestCarrito(TestCase):
    
    def test_agregar_producto_carrito(self, cliente_autenticado, producto_test):
        """Agregar producto al carrito"""
        response = cliente_autenticado.post(
            reverse('añadir_carrito', args=[producto_test.id]),
            {'cantidad': 1}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertTrue(CarritoItem.objects.filter(
            user=cliente_autenticado.user,
            producto=producto_test
        ).exists())
    
    def test_sumar_producto_carrito(self, cliente_autenticado, producto_test, carrito_item_test):
        """Sumar producto al carrito existente"""
        cantidad_inicial = carrito_item_test.cantidad
        
        response = cliente_autenticado.post(
            reverse('sumar_producto_al_carrito', args=[producto_test.id])
        )
        
        carrito_item_test.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(carrito_item_test.cantidad, cantidad_inicial + 1)
    
    def test_restar_producto_carrito(self, cliente_autenticado, producto_test, carrito_item_test):
        """Restar producto del carrito"""
        cantidad_inicial = carrito_item_test.cantidad
        
        response = cliente_autenticado.post(
            reverse('restar_producto_del_carrito', args=[producto_test.id])
        )
        
        carrito_item_test.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(carrito_item_test.cantidad, cantidad_inicial - 1)
    
    def test_eliminar_producto_carrito(self, cliente_autenticado, producto_test, carrito_item_test):
        """Eliminar producto del carrito"""
        response = cliente_autenticado.post(
            reverse('eliminar_producto_del_carrito', args=[producto_test.id])
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CarritoItem.objects.filter(
            user=cliente_autenticado.user,
            producto=producto_test
        ).exists())
    
    def test_ver_carrito(self, cliente_autenticado, carrito_item_test):
        """Visualización del carrito"""
        response = cliente_autenticado.get(reverse('ver_carrito'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/ver_carrito.html')
        self.assertContains(response, 'Martillo de Acero')
    
    def test_carrito_vacio(self, cliente_autenticado):
        """Carrito vacío muestra mensaje apropiado"""
        response = cliente_autenticado.get(reverse('ver_carrito'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'carrito vacío')  # Ajusta según tu template