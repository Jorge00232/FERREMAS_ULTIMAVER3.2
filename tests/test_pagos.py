import pytest
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from ferreteria.models import Order, CarritoItem

@pytest.mark.django_db
class TestPagos(TestCase):
    
    def test_procesar_compra_vista(self, cliente_autenticado, carrito_item_test):
        """Acceso a la vista de procesar compra"""
        response = cliente_autenticado.get(reverse('procesar_compra'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/procesar_compra.html')
    
    def test_procesar_compra_sin_productos(self, cliente_autenticado):
        """Intento de compra sin productos en el carrito"""
        response = cliente_autenticado.get(reverse('procesar_compra'))
        
        self.assertEqual(response.status_code, 200)
        # Verificar que muestra mensaje de carrito vacío o redirige
    
    @patch('ferreteria.views.Transaction')
    def test_procesar_compra_con_despacho(self, mock_transaction, cliente_autenticado, carrito_item_test):
        """Procesar compra con método de despacho"""
        mock_transaction.return_value.create.return_value = {
            'token': 'test_token_123',
            'url': 'https://webpay.test/redirect'
        }
        
        data = {
            'delivery_method': 'delivery',
            'delivery_address': 'Calle Test 123'
        }
        
        response = cliente_autenticado.post(reverse('procesar_compra'), data)
        
        # Verificar que se creó la orden
        order = Order.objects.filter(user=cliente_autenticado.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.delivery_method, 'delivery')
        self.assertEqual(order.delivery_address, 'Calle Test 123')