from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ⭐️ Importa las vistas de drf-spectacular (NUEVA ADICIÓN) ⭐️
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ⭐️ Rutas de la Documentación API (NUEVAS ADICIONES) ⭐️
    # 1. Ruta para el archivo de esquema OpenAPI (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Ruta para la interfaz interactiva de Swagger UI (RESUELVE EL 404)
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Optional: Redoc documentation interface
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    # Incluye todas las URLs de tu app 'core'.
    # Si usas namespace='core' asegúrate de que core/urls.py tenga: app_name = "core"
    path('', include(('core.urls', 'core'), namespace='core')),

    # Vistas de autenticación integradas de Django (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Servir archivos estáticos en desarrollo desde STATIC_ROOT (útil tras collectstatic)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)