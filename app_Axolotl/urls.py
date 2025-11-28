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
    path('admin_panel/productos/borrar/<int:producto_id>/', views.borrar_productos, name='borrar_productos'),

    # CRUD Artistas
    path('admin_panel/artistas/agregar/', views.agregar_artistas, name='agregar_artistas'),
    path('admin_panel/artistas/ver/', views.ver_artistas, name='ver_artistas'),
    path('admin_panel/artistas/actualizar/<int:artista_id>/', views.actualizar_artistas, name='actualizar_artistas'),
    path('admin_panel/artistas/borrar/<int:artista_id>/', views.borrar_artistas, name='borrar_artistas'),
    
    # CRUD Clientes
    path('admin_panel/clientes/ver/', views.ver_clientes, name='ver_clientes'),
    path('admin_panel/clientes/actualizar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('admin_panel/clientes/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # CRUD Empleados
    path('admin_panel/empleados/ver/', views.ver_empleados, name='ver_empleados'),
    path('admin_panel/empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('admin_panel/empleados/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('admin_panel/empleados/borrar/<int:empleado_id>/', views.borrar_empleado, name='borrar_empleado'),
    
    # CRUD Pedidos
    path('admin_panel/pedidos/ver/', views.ver_pedidos, name='ver_pedidos'),
    path('admin_panel/pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('admin_panel/pedidos/actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('admin_panel/pedidos/borrar/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
    
    # CRUD Detalles Pedidos
    path('admin_panel/detalles_pedidos/ver/', views.ver_detalles_pedidos, name='ver_detalles_pedidos'),
    path('admin_panel/detalles_pedidos/agregar/', views.agregar_detalle_pedido, name='agregar_detalle_pedido'),
    path('admin_panel/detalles_pedidos/actualizar/<int:detalle_id>/', views.actualizar_detalle_pedido, name='actualizar_detalle_pedido'),
    path('admin_panel/detalles_pedidos/borrar/<int:detalle_id>/', views.borrar_detalle_pedido, name='borrar_detalle_pedido'),
    
    # URLs del Frontend de AxolotlMusic
    path('', views.login_frontend, name='root_login'), # Root -> login
    path('login/', views.login_frontend, name='login_frontend'), # Página de login del frontend
    path('index/', views.index_frontend, name='index_frontend'), # Página principal del frontend
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('artistas/', views.artistas_frontend, name='artistas_frontend'),
    path('lista/', views.lista_frontend, name='lista_frontend'),
    path('comprar/', views.comprar_frontend, name='comprar_frontend'),
    path('genero/', views.genero_frontend, name='genero_frontend'),
    path('tipo/', views.tipo_frontend, name='tipo_frontend'),
    path('novedades/', views.novedades_frontend, name='novedades_frontend'),
    path('finalizar/', views.finalizar_frontend, name='finalizar_frontend'),
    path('cart/add/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.ver_carrito, name='ver_carrito'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # TODO: Añadir URLs para CRUD de Usuario, Pedido, DetallePedido
]

# Sirve archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)