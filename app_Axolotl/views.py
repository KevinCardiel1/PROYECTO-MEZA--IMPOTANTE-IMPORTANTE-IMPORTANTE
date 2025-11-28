from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import OperationalError
from .models import Producto, Artista, Usuario, Pedido, DetallePedido, Cart, CartItem
from .forms import ArtistaForm, ProductoForm, UsuarioForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


# ----------------------
# Autenticación y registro
# ----------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        account_type = request.POST.get('account_type')  # 'employee' o 'client'
        
        if not username or not email or not password or not account_type:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('register')

        # Crear usuario con is_staff basado en el tipo de cuenta
        is_staff = (account_type == 'employee')
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            is_staff=is_staff
        )
        
        # Si es empleado, agregarlo al grupo 'Empleados'
        if is_staff:
            group, _ = Group.objects.get_or_create(name='Empleados')
            user.groups.add(group)
        else:
            # Si es cliente, crear el perfil Usuario (se crea automáticamente por señal)
            pass
        
        messages.success(request, 'Cuenta creada correctamente. Por favor inicia sesión.')
        return redirect('login_frontend')

    return render(request, 'register.html')


def login_frontend(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Si es staff, enviarlo al panel de administración
            if user.is_staff:
                return redirect('inicio_axolotlmusic')
            return redirect('index_frontend')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login_frontend')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_frontend')


# ----------------------
# Comprobadores
# ----------------------
def is_staff_user(user):
    return user.is_staff


def _safe_clientes_list():
    """Devuelve un queryset de `Usuario` cuando la BD está actualizada,
    o una lista de diccionarios basada en `User` si falta la columna (migraciones pendientes).
    Esto evita que las vistas y plantillas rompan antes de aplicar `makemigrations`/`migrate`.
    """
    try:
        return Usuario.objects.filter(user__is_staff=False).order_by('nombre')
    except OperationalError:
        users = User.objects.filter(is_staff=False).order_by('username')
        return [
            {'id': u.id, 'nombre': u.username, 'email': u.email or '', 'tel': ''}
            for u in users
        ]


def _safe_all_usuarios():
    """Devuelve todos los usuarios de tipo `Usuario` o una lista basada en `User` como fallback."""
    try:
        return Usuario.objects.all()
    except OperationalError:
        users = User.objects.all().order_by('username')
        return [
            {'id': u.id, 'nombre': u.username, 'email': u.email or '', 'tel': ''}
            for u in users
        ]


# ----------------------
# Panel de administración
# ----------------------
@login_required
@user_passes_test(is_staff_user)
def inicio_axolotlmusic(request):
    try:
        clientes_count = Usuario.objects.count()
    except OperationalError:
        clientes_count = User.objects.filter(is_staff=False).count()
    artistas_count = Artista.objects.count()
    productos_count = Producto.objects.count()
    pedidos_count = Pedido.objects.count()
    context = {
        'clientes_count': clientes_count,
        'artistas_count': artistas_count,
        'productos_count': productos_count,
        'pedidos_count': pedidos_count,
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ----------------------
# CRUD Productos (Admin)
# ----------------------
@login_required
@user_passes_test(is_staff_user)
def agregar_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('ver_productos')
    else:
        form = ProductoForm()
    return render(request, 'admin_panel/productos_agregar.html', {'form': form})


@login_required
@user_passes_test(is_staff_user)
def ver_productos(request):
    productos = Producto.objects.select_related('artista').all().order_by('-id')
    return render(request, 'admin_panel/productos_ver.html', {'productos': productos})


@login_required
@user_passes_test(is_staff_user)
def actualizar_productos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('ver_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'admin_panel/productos_actualizar.html', {'form': form, 'producto': producto})


@login_required
@user_passes_test(is_staff_user)
def borrar_productos(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('ver_productos')
    return render(request, 'admin_panel/productos_borrar.html', {'producto': producto})


# ----------------------
# CRUD Artistas (Admin)
# ----------------------
@login_required
@user_passes_test(is_staff_user)
def agregar_artistas(request):
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artista agregado.')
            return redirect('ver_artistas')
    else:
        form = ArtistaForm()
    return render(request, 'artistas_admin/agregar_artistas.html', {'form': form})


@login_required
@user_passes_test(is_staff_user)
def ver_artistas(request):
    artistas = Artista.objects.all().order_by('nombre_artista')
    return render(request, 'artistas_admin/ver_artistas.html', {'artistas': artistas})


@login_required
@user_passes_test(is_staff_user)
def ver_clientes(request):
    # Mostrar solo usuarios que NO son staff/administradores
    clientes = _safe_clientes_list()
    return render(request, 'admin_panel/clientes_ver.html', {'clientes': clientes})


@login_required
@user_passes_test(is_staff_user)
def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Usuario, id=cliente_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('ver_clientes')
    else:
        form = UsuarioForm(instance=cliente)
    return render(request, 'admin_panel/clientes_actualizar.html', {'form': form, 'cliente': cliente})


@login_required
@user_passes_test(is_staff_user)
def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Usuario, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('ver_clientes')
    return render(request, 'admin_panel/clientes_borrar.html', {'cliente': cliente})


# ----------------------
# CRUD Empleados (Admin)
# ----------------------
@login_required
@user_passes_test(is_staff_user)
def ver_empleados(request):
    empleados = User.objects.filter(groups__name='Empleados') | User.objects.filter(is_staff=True)
    empleados = empleados.distinct().order_by('username')
    return render(request, 'admin_panel/empleados_ver.html', {'empleados': empleados})


@login_required
@user_passes_test(is_staff_user)
def agregar_empleado(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # asignar al grupo Empleados (crear si no existe)
            group, _ = Group.objects.get_or_create(name='Empleados')
            new_user.groups.add(group)
            # marcar staff si viene marcado
            if request.POST.get('is_staff') == 'on':
                new_user.is_staff = True
                new_user.save()
            messages.success(request, 'Empleado creado correctamente.')
            return redirect('ver_empleados')
    else:
        form = UserCreationForm()
    return render(request, 'admin_panel/empleados_form.html', {'form': form, 'user_obj': None})


@login_required
@user_passes_test(is_staff_user)
def actualizar_empleado(request, empleado_id):
    user_obj = get_object_or_404(User, id=empleado_id)
    if request.method == 'POST':
        # solo permitir cambiar email y staff flag aquí
        user_obj.email = request.POST.get('email', user_obj.email)
        user_obj.is_staff = True if request.POST.get('is_staff') == 'on' else False
        user_obj.save()
        messages.success(request, 'Empleado actualizado.')
        return redirect('ver_empleados')
    # Create a minimal form-like object for template rendering (we'll use UserCreationForm for adding only)
    form = None
    return render(request, 'admin_panel/empleados_form.html', {'form': form, 'user_obj': user_obj})


@login_required
@user_passes_test(is_staff_user)
def borrar_empleado(request, empleado_id):
    user_obj = get_object_or_404(User, id=empleado_id)
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, 'Empleado eliminado.')
        return redirect('ver_empleados')
    return render(request, 'admin_panel/empleados_borrar.html', {'user_obj': user_obj})


@login_required
@user_passes_test(is_staff_user)
def actualizar_artistas(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES, instance=artista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artista actualizado.')
            return redirect('ver_artistas')
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'artistas_admin/actualizar_artistas.html', {'form': form, 'artista': artista})


@login_required
@user_passes_test(is_staff_user)
def borrar_artistas(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    if request.method == 'POST':
        artista.delete()
        messages.success(request, 'Artista eliminado.')
        return redirect('ver_artistas')
    return render(request, 'artistas_admin/borrar_artistas.html', {'artista': artista})


# ----------------------
# Vistas Frontend (cliente)
# ----------------------
def index_frontend(request):
    # Mostrar novedades y artistas como ejemplo
    novedades = Producto.objects.filter(novedad=True).order_by('-id')[:8]
    artistas = Artista.objects.all().order_by('nombre_artista')
    return render(request, 'index_frontend.html', {'novedades': novedades, 'artistas': artistas})


def artistas_frontend(request):
    artistas_db = Artista.objects.all().order_by('nombre_artista')
    artistas_por_letra = {}
    for artista in artistas_db:
        inicial = artista.nombre_artista[0].upper()
        artistas_por_letra.setdefault(inicial, []).append(artista)

    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    artistas_final = {letra: artistas_por_letra.get(letra, []) for letra in alfabeto}
    return render(request, 'artistas_frontend.html', {'artistas_por_letra': artistas_final})


def lista_frontend(request):
    """Página simplificada de lista de artistas. Se actualizará automáticamente al agregar artistas en admin."""
    artistas = Artista.objects.all().order_by('nombre_artista')
    return render(request, 'lista.html', {'artistas': artistas})


def comprar_frontend(request):
    artista_nombre = request.GET.get('artista')
    if not artista_nombre:
        return redirect('artistas_frontend')

    artista_obj = get_object_or_404(Artista, nombre_artista=artista_nombre)
    productos = Producto.objects.filter(artista=artista_obj)
    vinilos = productos.filter(tipo__iexact='vinilo')
    cds = productos.filter(tipo__iexact='cd')
    cassettes = productos.filter(tipo__iexact='casete')

    context = {
        'artista': artista_obj,
        'vinilos': vinilos,
        'cds': cds,
        'cassettes': cassettes,
    }
    return render(request, 'comprar.html', context)


def genero_frontend(request):
    genero_param = request.GET.get('genero')
    if not genero_param:
        productos = Producto.objects.all().order_by('nombre_producto')
        genero_nombre = "Todos los Géneros"
    else:
        productos = Producto.objects.filter(genero__iexact=genero_param).order_by('nombre_producto')
        genero_nombre = genero_param

    vinilos = productos.filter(tipo__iexact='vinilo')
    cds = productos.filter(tipo__iexact='cd')
    cassettes = productos.filter(tipo__iexact='casete')

    context = {
        'genero_nombre': genero_nombre,
        'vinilos': vinilos,
        'cds': cds,
        'cassettes': cassettes,
    }
    return render(request, 'genero.html', context)


def tipo_frontend(request):
    """Página para filtrar productos por tipo (Vinilo, CD, Casete)."""
    tipo_param = request.GET.get('tipo', 'Vinilo')
    
    # Filtrar por tipo
    productos = Producto.objects.filter(tipo__iexact=tipo_param).order_by('nombre_producto')
    
    # Agrupar por artista
    productos_por_artista = {}
    for producto in productos:
        artista_nombre = producto.artista.nombre_artista
        if artista_nombre not in productos_por_artista:
            productos_por_artista[artista_nombre] = []
        productos_por_artista[artista_nombre].append(producto)
    
    tipo_nombre = tipo_param.capitalize()
    
    context = {
        'tipo_nombre': tipo_nombre,
        'tipo_param': tipo_param,
        'productos_por_artista': productos_por_artista,
        'todos_productos': productos,
    }
    return render(request, 'tipo.html', context)


def novedades_frontend(request):
    novedades = Producto.objects.filter(novedad=True).order_by('-id')[:4]
    return render(request, 'novedades.html', {'novedades': novedades})


def finalizar_frontend(request):
    artista_nombre = request.GET.get('artista')
    producto_nombre = request.GET.get('producto')
    precio = request.GET.get('precio')
    context = {
        'artista': artista_nombre,
        'producto': producto_nombre,
        'precio': precio,
    }
    return render(request, 'finalizar.html', context)


# ----------------------
# CARRITO (cliente)
# ----------------------
@login_required
def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    usuario = request.user.usuario
    cart, _ = Cart.objects.get_or_create(usuario=usuario)

    # cantidad desde POST (si no viene, 1)
    cantidad = int(request.POST.get('cantidad', 1)) if request.method == 'POST' else 1

    item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)
    if not created:
        item.cantidad = item.cantidad + cantidad
    else:
        item.cantidad = cantidad
    item.save()

    messages.success(request, f'"{producto.nombre_producto}" agregado al carrito.')
    # redirigir a la página anterior o al index
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/index/'
    return redirect(next_url)


@login_required
def ver_carrito(request):
    usuario = request.user.usuario
    cart, _ = Cart.objects.get_or_create(usuario=usuario)
    items = cart.items.select_related('producto').all()
    total = sum(item.subtotal() for item in items)
    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total': total})


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__usuario__user=request.user)
    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad <= 0:
                item.delete()
            else:
                item.cantidad = cantidad
                item.save()
            messages.success(request, 'Carrito actualizado.')
        except Exception:
            messages.error(request, 'Error al actualizar la cantidad.')
    return redirect('ver_carrito')


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__usuario__user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Producto eliminado del carrito.')
    return redirect('ver_carrito')


# ----------------------
# PERFIL DE USUARIO
# ----------------------
@login_required
def perfil_usuario(request):
    usuario = request.user.usuario
    pedidos = usuario.pedidos.order_by('-fecha')[:20]
    return render(request, 'perfil.html', {'usuario': usuario, 'pedidos': pedidos})


@login_required
def editar_perfil(request):
    usuario = request.user.usuario
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('perfil_usuario')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'perfil_editar.html', {'form': form})


# ----------------------
# CRUD Pedidos (Admin)
# ----------------------
@login_required
@user_passes_test(is_staff_user)
def ver_pedidos(request):
    pedidos = Pedido.objects.select_related('usuario').all().order_by('-fecha')
    return render(request, 'admin_panel/pedidos_ver.html', {'pedidos': pedidos})


@login_required
@user_passes_test(is_staff_user)
def agregar_pedido(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        cantidad_producto = request.POST.get('cantidad_producto')
        total = request.POST.get('total')
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            pedido = Pedido.objects.create(
                usuario=usuario,
                cantidad_producto=int(cantidad_producto),
                total=float(total)
            )
            messages.success(request, 'Pedido creado correctamente.')
            return redirect('ver_pedidos')
        except Exception as e:
            messages.error(request, f'Error al crear pedido: {str(e)}')
            
    usuarios = _safe_all_usuarios()
    return render(request, 'admin_panel/pedidos_agregar.html', {'usuarios': usuarios})


@login_required
@user_passes_test(is_staff_user)
def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.cantidad_producto = int(request.POST.get('cantidad_producto', pedido.cantidad_producto))
        pedido.total = float(request.POST.get('total', pedido.total))
        pedido.save()
        messages.success(request, 'Pedido actualizado correctamente.')
        return redirect('ver_pedidos')
    
    usuarios = _safe_all_usuarios()
    return render(request, 'admin_panel/pedidos_actualizar.html', {'pedido': pedido, 'usuarios': usuarios})


@login_required
@user_passes_test(is_staff_user)
def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado.')
        return redirect('ver_pedidos')
    return render(request, 'admin_panel/pedidos_borrar.html', {'pedido': pedido})


# ----------------------
# CRUD Detalles Pedidos (Admin)
# ----------------------
@login_required
@user_passes_test(is_staff_user)
def ver_detalles_pedidos(request):
    detalles = DetallePedido.objects.select_related('pedido', 'usuario', 'producto').all().order_by('-fecha')
    return render(request, 'admin_panel/detalles_pedidos_ver.html', {'detalles': detalles})


@login_required
@user_passes_test(is_staff_user)
def agregar_detalle_pedido(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido')
        usuario_id = request.POST.get('usuario')
        producto_id = request.POST.get('producto')
        cantidad_producto = request.POST.get('cantidad_producto')
        precio = request.POST.get('precio')
        total = request.POST.get('total')
        
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            usuario = Usuario.objects.get(id=usuario_id)
            producto = Producto.objects.get(id=producto_id)
            
            detalle = DetallePedido.objects.create(
                pedido=pedido,
                usuario=usuario,
                producto=producto,
                cantidad_producto=int(cantidad_producto),
                precio=float(precio),
                total=float(total)
            )
            messages.success(request, 'Detalle de pedido creado correctamente.')
            return redirect('ver_detalles_pedidos')
        except Exception as e:
            messages.error(request, f'Error al crear detalle: {str(e)}')
            
    pedidos = Pedido.objects.all()
    usuarios = _safe_all_usuarios()
    productos = Producto.objects.all()
    return render(request, 'admin_panel/detalles_pedidos_agregar.html', {
        'pedidos': pedidos,
        'usuarios': usuarios,
        'productos': productos
    })


@login_required
@user_passes_test(is_staff_user)
def actualizar_detalle_pedido(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    if request.method == 'POST':
        detalle.cantidad_producto = int(request.POST.get('cantidad_producto', detalle.cantidad_producto))
        detalle.precio = float(request.POST.get('precio', detalle.precio))
        detalle.total = float(request.POST.get('total', detalle.total))
        detalle.save()
        messages.success(request, 'Detalle actualizado correctamente.')
        return redirect('ver_detalles_pedidos')
    
    pedidos = Pedido.objects.all()
    usuarios = _safe_all_usuarios()
    productos = Producto.objects.all()
    return render(request, 'admin_panel/detalles_pedidos_actualizar.html', {
        'detalle': detalle,
        'pedidos': pedidos,
        'usuarios': usuarios,
        'productos': productos
    })


@login_required
@user_passes_test(is_staff_user)
def borrar_detalle_pedido(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Detalle de pedido eliminado.')
        return redirect('ver_detalles_pedidos')
    return render(request, 'admin_panel/detalles_pedidos_borrar.html', {'detalle': detalle})