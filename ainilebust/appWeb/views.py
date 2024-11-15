from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView

from datetime import date, datetime
import calendar
import json

from babel.dates import format_date, parse_date

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ReseñaForm,
    ContactForm,
    ProductoForm,
    PresupuestoForm,
    DisponibilidadForm,
)
from .models import Reseña, Producto, Disponibilidad


def register_view(request):
    """Registro de usuarios normales"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Por favor, corrige los errores.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Inicio de sesión para usuarios y admin"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redireccionar según rol
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario inválido. Revisa los datos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """Dashboard para el administrador"""
    user = request.user  # Usuario autenticado
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos han sido actualizados con éxito.')
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm(instance=user)

    return render(request, 'admin_dashboard.html', {'user': user, 'form': form})


@user_passes_test(lambda u: not u.is_superuser)
def user_dashboard(request):
    """Dashboard para usuarios normales"""
    return render(request, 'user_dashboard.html')


def index_view(request):
    return render(request, 'index.html')


def servicios(request):
    return render(request, 'servicios.html')


def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            send_mail(
                f'Mensaje de {nombre}',
                mensaje,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return redirect('contacto') 
    else:
        form = ContactForm()
    return render(request, 'contacto.html', {'form': form})


def sobre_nosotros(request):
    reseñas = Reseña.objects.all().order_by('-fecha')
    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sobre_nosotros')
    else:
        form = ReseñaForm()
    return render(request, 'sobre_nosotros.html', {'form': form, 'reseñas': reseñas})


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': 1,
            'imagen': producto.imagen.url if producto.imagen else ''
        }

    request.session['carrito'] = carrito
    return JsonResponse({'mensaje': 'Producto agregado al carrito'})


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        return JsonResponse({'mensaje': 'Producto eliminado del carrito'})
    return JsonResponse({'mensaje': 'Producto no encontrado en el carrito'}, status=404)


def mostrar_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})


def realizar_presupuesto(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('home')  # Redirige a la página principal si el carrito está vacío

    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())

    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            request.session['carrito'] = {}
            return redirect('presupuesto_exitoso')
    else:
        form = PresupuestoForm()

    return render(request, 'realizar_presupuesto.html', {'form': form, 'total': total, 'carrito': carrito})


def presupuesto_exitoso(request):
    return render(request, 'presupuesto_exitoso.html')



def generar_calendario():
    activate('es')
    calendario = {}
    year = date.today().year
    for mes in range(1, 13):
        nombre_mes = format_date(datetime(year, mes, 1), "MMMM", locale='es')
        dias_mes = calendar.monthcalendar(year, mes)
        days = []
        for week in dias_mes:
            for dia in week:
                if dia == 0:
                    continue
                try:
                    fecha = datetime(year, mes, dia).date()
                except ValueError:
                    continue
                try:
                    disponibilidad_dia = Disponibilidad.objects.get(fecha=fecha)
                    estado = disponibilidad_dia.estado
                except Disponibilidad.DoesNotExist:
                    estado = "no-disponible"
                days.append({"fecha": fecha, "estado": estado})
        
        calendario[nombre_mes.capitalize()] = days

    return calendario


def calendario_usuario(request):
    calendario = generar_calendario()
    return render(request, 'calendario_usuario.html', {'calendario': calendario})

@user_passes_test(lambda u: u.is_superuser)
def calendario_admin(request):
    calendario = generar_calendario()
    return render(request, 'calendario_admin.html', {'calendario': calendario})

@csrf_exempt
def editar_disponibilidad(request, fecha):
    try:
        # Parsear la fecha desde el formato YYYY-MM-DD
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError as e:
        return JsonResponse({"error": f"El formato de la fecha no es válido: {str(e)}"}, status=400)

    if request.method == 'POST':
        try:
            # Cargar el cuerpo de la solicitud JSON
            data = json.loads(request.body)
            nuevo_estado = data.get("nuevo_estado")

            if nuevo_estado not in ['disponible', 'ocupado', 'no-disponible']:
                return JsonResponse({"error": "Estado no válido."}, status=400)

            # Buscar o crear la disponibilidad correspondiente
            disponibilidad, created = Disponibilidad.objects.get_or_create(fecha=fecha_obj)

            # Actualizar el estado
            disponibilidad.estado = nuevo_estado
            disponibilidad.save()

            return JsonResponse({"success": True, "nuevo_estado": nuevo_estado, "created": created})
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Datos inválidos: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error al actualizar la disponibilidad: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido."}, status=405)

# Eliminar disponibilidad
def eliminar_disponibilidad(request, fecha):
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    disponibilidad = get_object_or_404(Disponibilidad, fecha=fecha_obj)

    if request.method == 'POST':
        disponibilidad.delete()
        messages.success(request, 'Disponibilidad eliminada.')
        return redirect('calendario_admin')

    return render(request, 'eliminar_disponibilidad.html', {'fecha': fecha})





class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'agregar_producto.html'
    success_url = reverse_lazy('index')


def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})


def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})


def editar_producto(request, id):
    return render(request, 'editar_producto.html')


def eliminar_producto(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('index')
    return redirect('index')



def prueba(request):
    productos = Producto.objects.all()
    return render(request,'admin_producto.html', {'productos': productos})