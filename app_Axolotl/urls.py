from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs del panel de administración
    path('admin_panel/', views.inicio_axolotlmusic, name='inicio_axolotlmusic'), # Home del panel
    
    # CRUD Productos (ya existentes)
    path('admin_panel/productos/agregar/', views.agregar_productos, name='agregar_productos'),
    path('admin_panel/productos/ver/', views.ver_productos, name='ver_productos'),
    path('admin_panel/productos/actualizar/<int:producto_id>/', views.actualizar_productos, name='actualizar_productos'),
    path('admin_panel/productos/realizar_actualizacion/<int:producto_id>/', views.realizar_actualizacion_productos, name='realizar_actualizacion_productos'),
    path('admin_panel/productos/borrar/<int:producto_id>/', views.borrar_productos, name='borrar_productos'),

    # CRUD Artistas
    path('admin_panel/artistas/agregar/', views.agregar_artistas, name='agregar_artistas'),
    path('admin_panel/artistas/ver/', views.ver_artistas, name='ver_artistas'),
    path('admin_panel/artistas/actualizar/<int:artista_id>/', views.actualizar_artistas, name='actualizar_artistas'),
    path('admin_panel/artistas/borrar/<int:artista_id>/', views.borrar_artistas, name='borrar_artistas'),
    
    # URLs del Frontend de AxolotlMusic
    path('', views.index_frontend, name='index_frontend'), # Página principal del frontend
    path('login/', views.login_frontend, name='login_frontend'), # Página de login del frontend
    path('artistas/', views.artistas_frontend, name='artistas_frontend'),
    path('comprar/', views.comprar_frontend, name='comprar_frontend'),
    path('genero/', views.genero_frontend, name='genero_frontend'),
    path('novedades/', views.novedades_frontend, name='novedades_frontend'),
    path('finalizar/', views.finalizar_frontend, name='finalizar_frontend'),

    # TODO: Añadir URLs para CRUD de Usuario, Pedido, DetallePedido
]

# Sirve archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)