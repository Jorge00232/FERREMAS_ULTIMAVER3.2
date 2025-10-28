from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import procesar_compra, confirm_order, order_success,confirmar_pago,exchange_rate_view,contactanos

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('subcategoria/<int:subcategoria_id>/', views.subcategoria_productos, name='subcategoria_productos'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/añadir/<int:producto_id>/', views.añadir_carrito, name='añadir_carrito'),
    path('sumar/<int:producto_id>/', views.sumar_producto_al_carrito, name='sumar_producto_al_carrito'),
    path('restar_producto_del_carrito/<int:producto_id>/', views.restar_producto_del_carrito, name='restar_producto_del_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto_del_carrito, name='eliminar_producto_del_carrito'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('exchange_rate_view/', views.exchange_rate_view, name='exchange_rate_view'),
    path('procesar_compra/', views.procesar_compra, name='procesar_compra'),
    path('order/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),
    path('order/<int:order_id>/success/', views.order_success, name='order_success'),
    path('iniciar_pago/', views.iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
    path('exito_pago/', views.exito_pago, name='exito_pago'),
    path('exito_contacto/', views.exito_contacto, name='exito_contacto'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)