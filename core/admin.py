#core/admin.py
from django.contrib import admin
from .models import Category, Supplier, Product, Customer, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','sku','category','supplier','price','stock','updated_at')
    list_filter = ('category','supplier')
    search_fields = ('name','sku','description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name','contact_email','phone')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('unit_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','status','total','created_at')
    inlines = [OrderItemInline]
    actions = ['mark_completed']
    def mark_completed(self, request, queryset):
        queryset.update(status='C')
    mark_completed.short_description = "Marcar pedidos como completados"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','phone')
