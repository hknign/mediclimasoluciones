from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout, get_backends
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from django.http import HttpResponse

from datetime import date, datetime
import calendar
import json

from babel.dates import format_date, parse_date

from .forms import (
    CustomUserCreationForm,
    ReseñaForm,
    ContactForm,
    ProductoForm,
    PresupuestoForm,
    ServicioForm
)
from .models import Reseña, Producto, Servicio, Carrito, ItemCarrito, Disponibilidad

from django.contrib.auth.forms import AuthenticationForm
from django.utils.module_loading import import_string

from django.views.decorators.http import require_http_methods


def get_user_backend(user):
    for backend in get_backends():
        if backend.get_user(user.pk):
            return f"{backend.__module__}.{backend.__class__.__name__}"
    return None

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = get_user_backend(user)
            if backend:
         
                login(request, user, backend=backend)
            else:
                login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                backend = get_user_backend(user)
                if backend:
                    login(request, user, backend=backend)
                else:
                    login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@require_http_methods(["GET", "POST"])
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Login')
    if request.method == 'GET':
        logout(request)
        return redirect('Login')


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    user = request.user
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
    return render(request, 'user_dashboard.html')

def index_view(request):
    return render(request, 'index.html')


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



class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'agregar_servicio.html'  
    success_url = reverse_lazy('index') 

def servicios(request):
    # Filtrar los servicios por categoría
    servicios_instalacion = Servicio.objects.filter(categoria='INSTALACION')
    servicios_mantenimiento = Servicio.objects.filter(categoria='MANTENIMIENTO')
    servicios_tecnico = Servicio.objects.filter(categoria='SOPORTE_TECNICO')

    todos = Servicio.objects.all()
    
    return render(request, 'servicios.html', {
        'servicios_instalacion': servicios_instalacion,
        'servicios_mantenimiento': servicios_mantenimiento,
        'servicios_tecnico': servicios_tecnico,
        'todos':todos,
    })


def agregar_servicio(request,servicio_id):
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('index') 
    else:
        form = ServicioForm()
    return render(request, 'agregar_servicio.html', {'form': form})

def eliminar_servicio(request, id):
    if request.method == 'POST':
        servicio = get_object_or_404(Servicio, id=id)
        servicio.delete()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect('index')
    return redirect('index')


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


def editar_producto(request, id=None):
    if request.method == 'POST': 
        id = request.POST.get('id')
        producto = Producto.objects.get(id=id)
        if 'imagen' in request.FILES and request.FILES['imagen']:
            producto.imagen = request.FILES['imagen']
        nombre = request.POST.get('nombre')
        if nombre:
            producto.nombre = nombre
        descripcion = request.POST.get('descripcion')
        if descripcion:
            producto.descripcion = descripcion
        precio = request.POST.get('precio')
        if precio:
            producto.precio = precio
        producto.save()
        return redirect('/prueba/')
    producto = Producto.objects.get(id=id)
    return render(request, 'editar_producto.html', {'p': producto})

def eliminar_producto(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('index')
    return redirect('index')

from .models import Producto, Servicio
from .cart import Cart

def add_to_cart(request, product_id=None, service_id=None):
    cart = Cart(request)
    if product_id:
        product = get_object_or_404(Producto, id=product_id)
        cart.add(product, is_product=True)
    elif service_id:
        service = get_object_or_404(Servicio, id=service_id)
        cart.add(service, is_product=False)
    return redirect('carrito')


def remove_from_cart(request, product_id=None, service_id=None):
    cart = Cart(request)
    if product_id:
        product = get_object_or_404(Producto, id=product_id)
        cart.remove(product, is_product=True)
    elif service_id:
        service = get_object_or_404(Servicio, id=service_id)
        cart.remove(service, is_product=False)
    return redirect('carrito')


def finalizar_compra(request):
    return render(request,'finalizar_compra.html')

def realizar_presupuesto(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('home')
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

def get_total_price_view(request):
    cart = Cart(request)
    total = cart.get_total_price()
    return JsonResponse({'total_carrito': float(total)})

def agregar_producto_al_carrito(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    cart.add(item=producto, is_product=True)
    return redirect('carrito')

def agregar_servicio_al_carrito(request, servicio_id):
    cart = Cart(request)
    servicio = get_object_or_404(Servicio, id=servicio_id)
    cart.add(item=servicio, is_product=False)
    return redirect('carrito')



def add_to_cart(request, item_id, item_type):
    cart = Cart(request)
    if item_type == 'producto':
        item = get_object_or_404(Producto, id=item_id)
    elif item_type == 'servicio':
        item = get_object_or_404(Servicio, id=item_id)
    cart.add(item, item_type)
    return redirect('index')  # Redirigir al index o a cualquier página que prefieras

def decrement_from_cart(request, item_id, item_type):
    cart = Cart(request)
    if item_type == 'producto':
        item = get_object_or_404(Producto, id=item_id)
    elif item_type == 'servicio':
        item = get_object_or_404(Servicio, id=item_id)
    cart.decrement(item)
    return redirect('view_cart')  # Redirigir a la vista del carrito

def remove_from_cart(request, item_id, item_type):
    cart = Cart(request)
    if item_type == 'producto':
        item = get_object_or_404(Producto, id=item_id)
    elif item_type == 'servicio':
        item = get_object_or_404(Servicio, id=item_id)
    cart.remove(item)
    return redirect('view_cart')  # Redirigir a la vista del carrito

def view_cart(request):
    cart = Cart(request)
    return render(request, 'cart/view_cart.html', {'cart': cart})



def carrito_view(request):
    cart = Cart(request)
    cart_items = []
    total_carrito = cart.get_total_price()  # Llama directamente el método de la clase Cart

    for item in cart:
        producto = item.get('item')  # Ajusta para que coincida con el key que devuelves en el iterador
        if producto:
            cart_items.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(item['price']),
                'cantidad': item['quantity'],
                'imagen_url': producto.imagen.url if producto.imagen else ''
            })

    return JsonResponse({
        'carrito_items': cart_items,
        'total_carrito': float(total_carrito),
    })


def dias_disponibles(request):
    disponibles = Disponibilidad.objects.filter(estado='disponible').values('fecha', 'estado')
    dias_list = list(disponibles)
    return JsonResponse(dias_list, safe=False)

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


def prueba(request):
    productos = Producto.objects.all()
    return render(request,'admin_producto.html', {'productos': productos})
