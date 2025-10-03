from django import forms
from .models import Categoria, SubCategoria, Ubicacion, Activo


class CategoriaForm(forms.ModelForm):
    """Formulario para Categoría"""
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            })
        }


class SubCategoriaForm(forms.ModelForm):
    """Formulario para SubCategoría"""
    class Meta:
        model = SubCategoria
        fields = ['nombre', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la subcategoría'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class UbicacionForm(forms.ModelForm):
    """Formulario para Ubicación"""
    class Meta:
        model = Ubicacion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la ubicación'
            })
        }


class ActivoForm(forms.ModelForm):
    """Formulario para Activo"""
    class Meta:
        model = Activo
        fields = [
            'subcategoria', 'marca', 'modelo', 'numero_serial',
            'codigo_inventario', 'usuario_asignado', 'ubicacion',
            'observaciones', 'estado'
        ]
        widgets = {
            'subcategoria': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_subcategoria'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca del activo'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo del activo'
            }),
            'numero_serial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de serie (opcional)'
            }),
            'codigo_inventario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único de inventario'
            }),
            'usuario_asignado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ubicacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class ActivoFilterForm(forms.Form):
    """Formulario para filtrar activos"""
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subcategoria = forms.ModelChoiceField(
        queryset=SubCategoria.objects.all(),
        required=False,
        empty_label="Todas las subcategorías",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all(),
        required=False,
        empty_label="Todas las ubicaciones",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + list(Activo.EstadoActivo.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por código, marca o modelo...'
        })
    )


class ReasignarActivoForm(forms.ModelForm):
    """Formulario para reasignar activo a otro usuario"""
    class Meta:
        model = Activo
        fields = ['usuario_asignado']
        widgets = {
            'usuario_asignado': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class ReubicarActivoForm(forms.ModelForm):
    """Formulario para reubicar activo"""
    class Meta:
        model = Activo
        fields = ['ubicacion']
        widgets = {
            'ubicacion': forms.Select(attrs={
                'class': 'form-select'
            })
        }


