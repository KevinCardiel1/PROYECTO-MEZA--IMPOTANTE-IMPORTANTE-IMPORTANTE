from django import forms
from .models import Artista, Producto, Usuario


class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        fields = ['nombre_artista', 'descripcion', 'foto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':4}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['artista', 'nombre_producto', 'genero', 'tipo', 'descripcion', 'stock', 'precio', 'novedad', 'img']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':3}),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'tel', 'direccion', 'codigo_postal', 'profile_image']
