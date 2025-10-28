from django.contrib import admin
from .models import Marca, Categoria, Subcategoria, Producto, CarritoItem, Order


# Registra los otros modelos en el admin

admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Producto)
admin.site.register(CarritoItem)
admin.site.register(Order)



