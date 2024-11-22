# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Reseña,Producto
from .models import Disponibilidad
from .models import CustomUser, Servicio

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name','email',"password1","password2" )


class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['nombre', 'email', 'comentario']


class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu email'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tu mensaje'}))



class PresupuestoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu email'}))
    telefono = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu teléfono'}))
    comentarios = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comentarios adicionales'}))



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['imagen', 'nombre', 'descripcion', 'precio']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ['fecha', 'estado']



class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen']
        # Widget de la categoría se define aquí
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
    
    # Campos personalizados
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio'}),
        max_length=255,
        required=True
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio'}),
        required=True
    )
    
    precio = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio del servicio'}),
        required=True,
        max_digits=10, decimal_places=2
    )
    
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True
    )

    # Este campo usa las opciones predefinidas de la categoría
    categoria = forms.ChoiceField(
        choices=Servicio.CATEGORIA_CHOICES,  # Asumiendo que CATEGORIAS se definió en el modelo
        widget=forms.Select(attrs={'class': 'form-control'})
    )