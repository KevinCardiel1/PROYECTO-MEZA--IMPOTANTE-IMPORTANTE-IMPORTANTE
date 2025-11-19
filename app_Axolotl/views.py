from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Artista, Usuario, Pedido, DetallePedido # Asegúrate de importar todos tus modelos

# ... (tus funciones existentes de productos) ...

# Funciones para el CRUD de Artistas
def agregar_artistas(request):
    if request.method == 'POST':
        nombre_artista = request.POST['nombre_artista']
        descripcion = request.POST['descripcion']
        Artista.objects.create(nombre_artista=nombre_artista, descripcion=descripcion)
        return redirect('ver_artistas')
    return render(request, 'artistas_admin/agregar_artistas.html')

def ver_artistas(request):
    artistas = Artista.objects.all()
    return render(request, 'artistas_admin/ver_artistas.html', {'artistas': artistas})

def actualizar_artistas(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    if request.method == 'POST':
        artista.nombre_artista = request.POST['nombre_artista']
        artista.descripcion = request.POST['descripcion']
        artista.save()
        return redirect('ver_artistas')
    return render(request, 'artistas_admin/actualizar_artistas.html', {'artista': artista})

def borrar_artistas(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    if request.method == 'POST':
        artista.delete()
        return redirect('ver_artistas')
    return render(request, 'artistas_admin/borrar_artistas.html', {'artista': artista})


# Vistas para el frontend de AxolotlMusic
def index_frontend(request):
    return render(request, 'index_frontend.html')

def login_frontend(request):
    return render(request, 'login.html')

def artistas_frontend(request):
    artistas_db = Artista.objects.all().order_by('nombre_artista')
    # Prepara los artistas por letra inicial
    artistas_por_letra = {}
    for artista in artistas_db:
        inicial = artista.nombre_artista[0].upper()
        if inicial not in artistas_por_letra:
            artistas_por_letra[inicial] = []
        artistas_por_letra[inicial].append(artista)
    
    # Asegúrate de que todas las letras del alfabeto estén presentes, incluso si no tienen artistas
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    artistas_final = {}
    for letra in alfabeto:
        artistas_final[letra] = artistas_por_letra.get(letra, [])

    return render(request, 'artistas_frontend.html', {'artistas_por_letra': artistas_final})

def comprar_frontend(request):
    artista_nombre = request.GET.get('artista')
    if not artista_nombre:
        return redirect('artistas_frontend') # Redirigir si no hay artista
    
    artista_obj = get_object_or_404(Artista, nombre_artista=artista_nombre)
    productos = Producto.objects.filter(artista=artista_obj) # Obtiene todos los productos del artista
    
    # Aquí puedes categorizar los productos si quieres (vinilos, cds, cassettes)
    vinilos = productos.filter(tipo__iexact='vinilo')
    cds = productos.filter(tipo__iexact='cd')
    cassettes = productos.filter(tipo__iexact='casete') # O 'cassette' si usas esa convención

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
        # Si no se especifica un género, podrías mostrar todos los productos
        productos = Producto.objects.all().order_by('nombre_producto')
        genero_nombre = "Todos los Géneros"
    else:
        # Filtra productos por el género dado
        productos = Producto.objects.filter(genero__iexact=genero_param).order_by('nombre_producto')
        genero_nombre = genero_param

    # Categoriza los productos por tipo (Vinilo, CD, Cassette)
    vinilos = productos.filter(tipo__iexact='vinilo')
    cds = productos.filter(tipo__iexact='cd')
    cassettes = productos.filter(tipo__iexact='casete') # O 'cassette'

    context = {
        'genero_nombre': genero_nombre,
        'vinilos': vinilos,
        'cds': cds,
        'cassettes': cassettes,
    }
    return render(request, 'genero.html', context)


def novedades_frontend(request):
    novedades = Producto.objects.filter(novedad=True).order_by('-id')[:4] # Obtener las 4 novedades más recientes
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


# TODO: Añadir vistas CRUD para Usuario, Pedido, DetallePedido