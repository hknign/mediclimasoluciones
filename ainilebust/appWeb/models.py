from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model


from django.core.validators import MinValueValidator, MaxValueValidator


def get_default_user():
    User = get_user_model()
    return User.objects.first().id if User.objects.exists() else None

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = extra_fields.get('is_staff', False)
        user.is_superuser = extra_fields.get('is_superuser', False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Default should be False for regular users

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Reseña(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    valoracion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,  # Valor predeterminado para filas existentes
        help_text="La valoración debe estar entre 1 y 5."
    )


    def __str__(self):
        return f"{self.nombre} - {self.fecha.strftime('%Y-%m-%d')} - {self.valoracion} estrellas"


class Disponibilidad(models.Model):
    fecha = models.DateField(unique=True, default=date.today)
    estado = models.CharField(max_length=50, choices=[
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('no_disponible', 'No disponible'),
    ])

    def __str__(self):
        return f"{self.fecha} - {self.estado}"

class Producto(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    favorito = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('INSTALACION', 'Instalación'),
        ('MANTENIMIENTO', 'Mantenimiento'),
        ('SOPORTETECNICO', 'Soporte Técnico'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='INSTALACION')
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrito'
    )

    def __str__(self):
        return f"Carrito de {self.usuario.email}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(
        'Producto',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    servicio = models.ForeignKey(
        'Servicio',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.producto:
            self.servicio = None
        elif self.servicio:
            self.producto = None
        super(ItemCarrito, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto if self.producto else self.servicio} - {self.cantidad}"

class SobreNosotros(models.Model):
    contenido = models.TextField(default="En Mediclimasoluciones, nos especializamos en la venta, instalación y mantenimiento de equipos médicos de alta calidad de la marca BIOBASE.")

    def __str__(self):
        return "Sobre Nosotros"

class Pregunta(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Relación con el modelo de usuario
        on_delete=models.SET_NULL,  # Si el autor es eliminado, se pone como NULL
        null=True,
        blank=True
    )
    contenido = models.TextField()  # Contenido de la pregunta
    respuesta = models.TextField(null=True, blank=True)  # Respuesta a la pregunta
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de la pregunta

    def __str__(self):
        return self.contenido[:50]
