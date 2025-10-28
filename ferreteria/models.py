from django.db import models
from django.contrib.auth.models import User
import random

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100, blank=True)  # Sin unique=True temporalmente

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    codigo_producto = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo_producto:
            self.codigo_producto = self.generate_codigo_producto()
        super().save(*args, **kwargs)

    def generate_codigo_producto(self):
        return f"FER-{random.randint(10000, 99999)}"

    def __str__(self):
        return self.nombre

class CarritoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    webpay_token = models.CharField(max_length=200, blank=True, null=True)
    webpay_url = models.URLField(blank=True, null=True)
    delivery_method = models.CharField(max_length=20, choices=[('pickup', 'Retiro en tienda'), ('delivery', 'Despacho a domicilio')], default='pickup')
    delivery_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"