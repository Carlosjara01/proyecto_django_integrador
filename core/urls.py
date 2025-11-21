from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Products
    path('productos/', views.ProductListView.as_view(), name='product_list'),
    path('productos/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('productos/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('productos/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('productos/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Orders
    path('pedidos/', views.OrderListView.as_view(), name='order_list'),
    path('pedidos/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('pedidos/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('pedidos/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),

    # Authentication
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Utilities
    path('search/', views.search_view, name='search'),
    path('export/csv/', views.export_products_csv, name='export_csv'),
    path('export/pdf/', views.export_products_pdf, name='export_pdf'),
    path('api/productos/', views.api_productos, name='api_productos'),

    # Home / Root
    path('', views.home_view, name='base'),
]
