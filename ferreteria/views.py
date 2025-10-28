from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria, Subcategoria, CarritoItem, Order, Marca
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, CustomUserCreationForm, DeliveryForm, CustomAuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from rest_framework import viewsets
from .serializers import CategoriaSerializer, SubcategoriaSerializer, ProductoSerializer, CarritoItemSerializer, OrderSerializer, MarcaSerializer
import requests
from .webpay_config import Transaction
from transbank.webpay.webpay_plus.transaction import Transaction as WebpayTransaction
from datetime import datetime


def index(request):
    productos_destacados = Producto.objects.order_by('?')[:6]  # Obtén 5 productos aleatorios
    return render(request, 'ferreteria/index.html', {'productos_destacados': productos_destacados})

def catalogo(request):
    categorias = Categoria.objects.all()
    return render(request, 'ferreteria/catalogo.html', {'categorias': categorias})

def subcategoria_productos(request, subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_id)
    productos = Producto.objects.filter(subcategoria=subcategoria)
    return render(request, 'ferreteria/subcategoria_productos.html', {'subcategoria': subcategoria, 'productos': productos})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'ferreteria/producto_detalle.html', {'producto': producto})

@login_required
def añadir_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    item_carrito, creado = CarritoItem.objects.get_or_create(
        producto=producto,
        user=request.user,
    )
    if creado:
        item_carrito.cantidad = request.POST.get('cantidad', 1)
    else:
        item_carrito.cantidad += int(request.POST.get('cantidad', 1))
    item_carrito.save()
    return redirect('ver_carrito')

@login_required
def sumar_producto_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito_item, created = CarritoItem.objects.get_or_create(
        user=request.user, 
        producto=producto,
        defaults={'cantidad': 1}
    )
    # Verificar si hay suficiente stock para añadir otro producto al carrito
    if producto.stock > carrito_item.cantidad:
        carrito_item.cantidad += 1
        carrito_item.save()
    else:
        messages.warning(request, f"No hay suficiente stock disponible para {producto.nombre}.")
    
    return redirect('ver_carrito')

@login_required
def restar_producto_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito_item = get_object_or_404(CarritoItem, user=request.user, producto=producto)
    if carrito_item.cantidad > 1:
        carrito_item.cantidad -= 1
        carrito_item.save()
    else:
        carrito_item.delete()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito_items = CarritoItem.objects.filter(user=request.user)
    total_amount = sum(item.producto.precio * item.cantidad for item in carrito_items)
    return render(request, 'ferreteria/ver_carrito.html', {
        'carrito_items': carrito_items,
        'total_amount': total_amount
    })

@login_required
def eliminar_producto_del_carrito(request, producto_id):
    item = get_object_or_404(CarritoItem, producto_id=producto_id, user=request.user)
    item.delete()
    return redirect('ver_carrito')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'ferreteria/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=username_or_email)
                username = user.username
            except UserModel.DoesNotExist:
                username = username_or_email
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Correo electrónico o contraseña incorrectos")
        else:
            form.add_error(None, "Formulario no válido. Por favor revisa los datos ingresados.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'ferreteria/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def contactanos(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            send_mail(
                f'Nuevo contacto de: {nombre}',
                f'Mensaje: {mensaje}\nCorreo: {email}',
                'ferremas.2024@outlook.com',
                ['ferremas.2024@outlook.com'],
                fail_silently=False,
            )
            messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
            return redirect('exito_contacto')
    else:
        form = ContactForm()
    return render(request, 'ferreteria/contactanos.html', {'form': form})

def exito_contacto(request):
    return render(request, 'ferreteria/exito_contacto.html')

@login_required
def procesar_compra(request):
    user = request.user
    carrito_items = CarritoItem.objects.filter(user=user)
    total_amount = sum(item.producto.precio * item.cantidad for item in carrito_items)
    delivery_fee = 5000  # Monto extra por despacho

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery_method = form.cleaned_data['delivery_method']
            delivery_address = form.cleaned_data['delivery_address']
            if delivery_method == 'delivery':
                delivery_fee = 5000  # Ajusta el monto extra por despacho según tus necesidades
                total_amount += delivery_fee

            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                delivery_method=delivery_method,
                delivery_address=delivery_address if delivery_method == 'delivery' else ''
            )

            buy_order = str(user.id) + str(order.id) + 'B123'
            session_id = str(user.id)
            return_url = request.build_absolute_uri('/ferreteria/confirmar_pago/')

            transaction = Transaction()
            try:
                response = transaction.create(buy_order=buy_order, session_id=session_id, amount=total_amount, return_url=return_url)

                if response:
                    order.webpay_token = response.token                    # ← response.token (sin corchetes)
                    order.webpay_url = response.url                        # ← response.url (sin corchetes)
                    order.save()
                    return redirect(response.url + '?token_ws=' + response.token)  # ← response.url y response.token
                else:
                    return HttpResponse("Error al iniciar la transacción con WebPay")
            except Exception as e:
                return HttpResponse(f"Error al iniciar la transacción con WebPay: {e}")
    else:
        form = DeliveryForm()

    return render(request, 'ferreteria/procesar_compra.html', {'form': form, 'total_amount': total_amount, 'delivery_fee': delivery_fee})

def confirm_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if 'token_ws' in request.GET:
        order.webpay_token = request.GET['token_ws']
        order.save()
        return redirect('order_success', order_id=order.id)
    return render(request, 'ferreteria/error.html', {'message': 'Hubo un problema al confirmar la transacción con WebPay.'})

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'ferreteria/order_success.html', {'order': order})

@login_required
@login_required
def confirmar_pago(request):
    token = request.GET.get('token_ws')
    try:
        if not token:
            raise ValueError("Token not found in request")
        transaction = Transaction()
        response = transaction.commit(token=token)

        if response.status == 'AUTHORIZED':  # ← CAMBIADO: response.status en lugar de response.get('status')
            # Obtener la orden correspondiente
            order = get_object_or_404(Order, webpay_token=token)

            # Obtener los items del carrito antes de eliminarlos
            carrito_items = CarritoItem.objects.filter(user=order.user)
            productos_comprados = []
            for item in carrito_items:
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()
                productos_comprados.append({
                    'nombre': producto.nombre,
                    'cantidad': item.cantidad,
                    'precio': producto.precio,
                    'total': producto.precio * item.cantidad,
                })

            # Eliminar los items del carrito después de la confirmación exitosa
            carrito_items.delete()

            fecha_original = response.transaction_date  # ← CAMBIADO: response.transaction_date en lugar de response.get('transaction_date')
            fecha_datetime = datetime.strptime(fecha_original, '%Y-%m-%dT%H:%M:%S.%fZ')
            fecha_formateada = fecha_datetime.strftime('%d-%m-%Y')

            compra_datos = {
                'orden_compra': response.buy_order,  # ← CAMBIADO: response.buy_order
                'monto': response.amount,  # ← CAMBIADO: response.amount
                'codigo_autorizacion': response.authorization_code,  # ← CAMBIADO: response.authorization_code
                'fecha': fecha_formateada,
                'productos': productos_comprados,
                'metodo_entrega': order.delivery_method,
                'direccion_entrega': order.delivery_address if order.delivery_method == 'delivery' else 'N/A',
            }
            return render(request, 'ferreteria/exito_pago.html', {'response': response, 'compra_datos': compra_datos})
        else:
            return render(request, 'ferreteria/error_pago.html', {'error': 'Transacción no autorizada', 'response': response})
    except Exception as e:
        print(f"Error al confirmar la transacción con WebPay: {e}")
        return render(request, 'ferreteria/error_pago.html', {'error': str(e)})
    
    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = CarritoItem.objects.all()
    serializer_class = CarritoItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

def exchange_rate_view(request):
    try:
        response = requests.get('https://mindicador.cl/api')
        if response.status_code == 200:
            data = response.json()
            relevant_data = {
                'usd': data['dolar']['valor'],
                'eur': data['euro']['valor'],
            }
            return JsonResponse(relevant_data)
        else:
            return JsonResponse({'error': 'Failed to retrieve data'}, status=500)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def iniciar_pago(request):
    buy_order = "ordenCompra12345678"
    session_id = request.session.session_key
    amount = 10000
    return_url = settings.WEBPAY_RETURN_URL
    
    response = Transaction.create(buy_order, session_id, amount, return_url)
    return redirect(response['url'] + '?token_ws=' + response['token'])

def exito_pago(request):
    return render(request, 'ferreteria/exito_pago.html')