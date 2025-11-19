from django.db import models

# ======================
# MODELO USUARIO
# ======================
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200)
    codigo_postal = models.IntegerField()

    def __str__(self):
        return self.nombre


# ======================
# MODELO ARTISTA
# ======================
class Artista(models.Model):
    nombre_artista = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='artistas_fotos/', blank=True, null=True) # Nuevo campo

    def __str__(self):
        return self.nombre_artista


# ======================
# MODELO PRODUCTO
# ======================
class Producto(models.Model):
    artista = models.ForeignKey(
        Artista, on_delete=models.CASCADE, related_name='productos'
    )  # Relación 1-N (un artista puede tener muchos productos)

    nombre_producto = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    novedad = models.BooleanField(default=False)
    img = models.ImageField(upload_to='productos_img/', blank=True, null=True) # Nuevo campo

    def __str__(self):
        return f"{self.nombre_producto} - ${self.precio}"


# ======================
# MODELO PEDIDO
# ======================
class Pedido(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='pedidos'
    )  # Relación 1-N (un usuario puede tener muchos pedidos)

    cantidad_producto = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.nombre}"


# ======================
# MODELO DETALLE_PEDIDO
# ======================
class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='detalles'
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='detalles_pedido'
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='detalles'
    )

    cantidad_producto = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle #{self.id} - {self.producto.nombre_producto} ({self.cantidad_producto})"