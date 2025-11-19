from django.contrib import admin
from .models import Usuario, Artista, Producto, Pedido, DetallePedido

admin.site.register(Usuario)
admin.site.register(Artista)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)