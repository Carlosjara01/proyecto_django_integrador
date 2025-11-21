from django import forms
from .models import Product, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku','name','description','category','supplier','price','stock']
    def clean_price(self):
        p = self.cleaned_data.get('price')
        if p <= 0:
            raise forms.ValidationError("El precio debe ser mayor que 0.")
        return p

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer','status']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username","email","first_name","last_name","password1","password2")
