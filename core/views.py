# core/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from .models import Product, Order, Customer, Supplier, Category
from .forms import ProductForm, OrderForm, RegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
import csv
from reportlab.pdfgen import canvas
from django.contrib.auth.models import Group
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db import transaction

# ⭐️ Importaciones de Django REST Framework (NUEVO) ⭐️
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductAPISerializer # Importamos el nuevo serializador

# ---------------------------------------------------------------------
# StaffRequiredMixin mejorado
# ---------------------------------------------------------------------
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            login_url = reverse('core:login')
            return redirect(f"{login_url}?next={self.request.path}")
        messages.error(self.request, "Acceso denegado: necesitas permisos de administrador (staff).")
        return redirect('core:product_list')

# ---------------------------------------------------------------------
# Product CBVs
# (Vistas de productos existentes, sin cambios)
# ---------------------------------------------------------------------
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'core/product_list.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset().select_related('category', 'supplier')
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        supplier = self.request.GET.get('supplier')
        pmin = self.request.GET.get('pmin')
        pmax = self.request.GET.get('pmax')
        if q:
            qs = qs.filter(name__icontains=q)
        if cat:
            qs = qs.filter(category__id=cat)
        if supplier:
            qs = qs.filter(supplier__id=supplier)
        if pmin:
            try:
                qs = qs.filter(price__gte=Decimal(pmin))
            except Exception:
                pass
        if pmax:
            try:
                qs = qs.filter(price__lte=Decimal(pmax))
            except Exception:
                pass
        return qs.order_by('-updated_at')

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product_list')

    def form_valid(self, form):
        messages.success(self.request, "Producto creado con éxito.")
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product_list')

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado.")
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'core/product_confirm_delete.html'
    success_url = reverse_lazy('core:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado.")
        return super().delete(request, *args, **kwargs)

# ---------------------------------------------------------------------
# Order CBVs
# (Vistas de pedidos existentes, sin cambios)
# ---------------------------------------------------------------------
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().select_related('customer__user')
        return Order.objects.filter(customer__user=self.request.user).select_related('customer__user')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('core:order_list')

    def form_valid(self, form):
        if not self.request.user.is_staff:
            try:
                customer = Customer.objects.get(user=self.request.user)
                form.instance.customer = customer
            except Customer.DoesNotExist:
                messages.error(self.request, "No se encontró el perfil de cliente. Contactá al administrador.")
                return redirect('core:order_list')
        messages.success(self.request, "Pedido creado.")
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('core:order_list')

    def form_valid(self, form):
        messages.success(self.request, "Pedido actualizado.")
        return super().form_valid(form)

# ---------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------
class RegisterView(FormView):
    template_name = 'core/auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('core:product_list')

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        Customer.objects.create(user=user)
        group, _ = Group.objects.get_or_create(name='Clientes')
        user.groups.add(group)
        messages.success(self.request, "Registro exitoso. Ya puedes iniciar sesión.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'core/auth/login.html'

class CustomLogoutView(LogoutView):
    http_method_names = ['post']
    next_page = reverse_lazy('core:login')

# ---------------------------------------------------------------------
# Search view
# ---------------------------------------------------------------------
@login_required
def search_view(request):
    q = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if q:
        products = Product.objects.filter(name__icontains=q)[:20]
    return render(request, 'core/search_results.html', {'products': products, 'query': q})

# ---------------------------------------------------------------------
# Export CSV / PDF
# (Funciones existentes, sin cambios)
# ---------------------------------------------------------------------
@login_required
def export_products_csv(request):
    if not request.user.is_staff:
        messages.error(request, "Acceso denegado: permisos de staff requeridos para exportar.")
        return redirect('core:product_list')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'sku', 'name', 'category', 'supplier', 'price', 'stock'])
    for p in Product.objects.select_related('category', 'supplier').all():
        writer.writerow([
            p.id,
            p.sku,
            p.name,
            p.category.name if p.category else '',
            p.supplier.name if p.supplier else '',
            str(p.price),
            p.stock
        ])
    return response

@login_required
def export_products_pdf(request):
    if not request.user.is_staff:
        messages.error(request, "Acceso denegado: permisos de staff requeridos para exportar.")
        return redirect('core:product_list')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'
    pdf = canvas.Canvas(response)
    y = 800
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, y, "Listado de productos")
    y -= 30
    pdf.setFont("Helvetica", 10)
    for prod in Product.objects.all():
        line = f"{prod.id} - {prod.name} - {prod.price} - Stock: {prod.stock}"
        pdf.drawString(50, y, line)
        y -= 15
        if y < 50:
            pdf.showPage()
            y = 800
            pdf.setFont("Helvetica", 10)
    pdf.showPage()
    pdf.save()
    return response

# ---------------------------------------------------------------------
# ⭐️ API endpoint DRF (ACTUALIZADO) ⭐️
# ---------------------------------------------------------------------
@api_view(['GET']) # 1. Usamos el decorador de DRF
@login_required
def api_productos(request):
    """
    Retorna una lista de todos los productos disponibles en la tienda.
    Requiere que el usuario esté autenticado.
    """
    qs = Product.objects.select_related('category', 'supplier').all()
    
    # 2. Usamos el Serializador para transformar el QuerySet
    serializer = ProductAPISerializer(qs, many=True)
    
    # 3. Retornamos la respuesta usando Response de DRF, que maneja el JSON
    return Response({'productos': serializer.data})

@login_required
def home_view(request):
    return render(request, 'core/base.html')