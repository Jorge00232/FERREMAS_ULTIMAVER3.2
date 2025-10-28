from django import forms
from .models import Producto
from .models import CarritoItem, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    rut = forms.CharField(max_length=12, required=True, help_text="RUT sin puntos y con guion")
    Nombre = forms.CharField(max_length=30, required=True, help_text="Nombre")
    Apellido = forms.CharField(max_length=30, required=True, help_text="Apellido")

    class Meta:
        model = User
        fields = ('Nombre','Apellido','username', 'rut', 'email', 'password1', 'password2')

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not self.validate_rut(rut):
            raise forms.ValidationError("RUT inválido")
        return rut

    def validate_rut(self, rut):
        return True

class ProductoImagenForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['imagen']


class AñadirCarritoForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = ['cantidad']


class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    asunto = forms.CharField(max_length=100)
    mensaje = forms.CharField(widget=forms.Textarea)

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_method', 'delivery_address']
        widgets = {
            'delivery_method': forms.RadioSelect,
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        delivery_address = cleaned_data.get('delivery_address')

        if delivery_method == 'delivery' and not delivery_address:
            self.add_error('delivery_address', 'Por favor, ingrese una dirección para el despacho.')

        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Correo electrónico o nombre de usuario",
        widget=forms.TextInput(attrs={"autofocus": True})
    )