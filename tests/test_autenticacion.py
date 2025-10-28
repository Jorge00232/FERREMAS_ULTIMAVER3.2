import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ferreteria.forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()

@pytest.mark.django_db
class TestAutenticacion(TestCase):
    
    def test_registro_usuario_exitoso(self):
        """Cliente se registra en el sistema exitosamente"""
        data = {
            'Nombre': 'Juan',
            'Apellido': 'Pérez',
            'username': 'juanperez',
            'rut': '12345678-9',
            'email': 'juan@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
        
        # Verificar que se puede crear el usuario
        user = form.save()
        self.assertEqual(user.first_name, 'Juan')
        self.assertEqual(user.email, 'juan@example.com')
    
    def test_registro_contrasena_debil(self):
        """Registro del cliente con contraseña débil"""
        data = {
            'Nombre': 'Juan',
            'Apellido': 'Pérez',
            'username': 'juanperez',
            'rut': '12345678-9',
            'email': 'juan@example.com',
            'password1': '123',  # Contraseña débil
            'password2': '123'
        }
        
        form = CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_registro_correo_existente(self):
        """Registro con correo ya existente"""
        # Crear usuario primero
        User.objects.create_user(
            username='existente',
            email='existente@example.com',
            password='testpass123'
        )
        
        data = {
            'Nombre': 'Juan',
            'Apellido': 'Pérez',
            'username': 'juanperez',
            'rut': '12345678-9',
            'email': 'existente@example.com',  # Email ya existe
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        
        form = CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_login_credenciales_validas(self, usuario_test):
        """Inicio de sesión con credenciales válidas"""
        form = CustomAuthenticationForm(data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_login_credenciales_invalidas(self):
        """Inicio de sesión con credenciales inválidas"""
        form = CustomAuthenticationForm(data={
            'username': 'noexiste',
            'password': 'wrongpassword'
        })
        self.assertFalse(form.is_valid())
    
    def test_vista_registro(self, client):
        """Test de la vista de registro"""
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/register.html')
    
    def test_vista_login(self, client):
        """Test de la vista de login"""
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ferreteria/login.html')