from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ======================
# MODELO USUARIO
# ======================
class Usuario(models.Model):
    # Vincula el perfil con el User de Django para usar autenticación estándar
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    codigo_postal = models.IntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else self.nombre or self.email


# Crear/actualizar perfil automáticamente al crear User
@receiver(post_save, sender=User)
def create_or_update_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance, email=instance.email, nombre=instance.username)
    else:
        # Actualizar email/nombre si ya existe perfil
        try:
            perfil = instance.usuario
            perfil.email = instance.email
            perfil.nombre = instance.username
            perfil.save()
        except Usuario.DoesNotExist:
            Usuario.objects.create(user=instance, email=instance.email, nombre=instance.username)


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


# ======================
# CARRITO DE COMPRAS
# ======================
class Cart(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cart')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito - {self.usuario.nombre or self.usuario.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    added = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto}"