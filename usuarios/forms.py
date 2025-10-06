from django import forms
from .models import UsuarioAsignado


class UsuarioForm(forms.ModelForm):
    """Formulario para UsuarioAsignado"""
    
    class Meta:
        model = UsuarioAsignado
        fields = [
            'nombres', 'apellidos', 'identificacion', 'email', 
            'telefono', 'cargo', 'departamento', 'activo'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres del usuario'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos del usuario'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de identificación'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo del usuario'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Departamento'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el campo email opcional
        self.fields['email'].required = False
        self.fields['telefono'].required = False
        self.fields['cargo'].required = False
        self.fields['departamento'].required = False
