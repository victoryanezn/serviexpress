from django import forms
from .models import Servicio, Promocion, Proveedor, TipoProveedor
from django.forms.widgets import DateInput
from django.core.validators import MinValueValidator, MaxValueValidator



class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control fw-semibold'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control fw-semibold'}),
            'tipo_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'productos': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria_proveedor': forms.Select(attrs={'class': 'form-control'}),
        }

        
class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'porcentaje_descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    porcentaje_descuento = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    

class ProveedorFilterForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar proveedores...'}))
    tipo_proveedor = forms.ModelChoiceField(queryset=TipoProveedor.objects.all(), required=False, empty_label="Todos los tipos", widget=forms.Select(attrs={'class': 'form-control'}))