from rest_framework import serializers
from .models import Product

# Serializador para el endpoint /api/productos/
class ProductAPISerializer(serializers.ModelSerializer):
    # Campos que son relaciones (Category, Supplier) deben ser representados
    # por su nombre, no solo por su ID.
    category = serializers.CharField(source='category.name', allow_null=True, read_only=True)
    supplier = serializers.CharField(source='supplier.name', allow_null=True, read_only=True)
    
    # El campo 'price' es Decimal, lo convertimos a String para mantener la compatibilidad 
    # con tu implementación original de JsonResponse (aunque DRF lo manejaría mejor por defecto).
    price = serializers.CharField() 

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'supplier', 'price', 'stock']