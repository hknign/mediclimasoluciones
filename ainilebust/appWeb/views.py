# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReseñaForm, ContactForm
from django.contrib import messages
from .models import Reseña
from django.core.mail import send_mail
from django.conf import settings
from .models import Producto
from django.http import JsonResponse
from .forms import PresupuestoForm
from django.utils.translation import activate
import calendar
from datetime import date, datetime
from babel.dates import format_date

def register_view(request):
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
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario inválido. Revisa los datos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def index_view(request):
    return render(request,'index.html')

def productos(request):
    return render(request,'productos.html')

def servicios(request):
    return render(request,'servicios.html')


def contacto(request):
    return render(request,'contacto.html')

def sobre_nosotros(request):
    reseñas = Reseña.objects.all().order_by('-fecha')
    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sobre_nosotros')
    else:
        form = ReseñaForm()
    
    context = {
        'form': form,
        'reseñas': reseñas,
    }
    return render(request, 'sobre_nosotros.html', context)

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
            # Procesar el presupuesto aquí (calcular mano de obra, enviar correo, etc.)
            request.session['carrito'] = {}
            return redirect('presupuesto_exitoso')
    else:
        form = PresupuestoForm()

    return render(request, 'realizar_presupuesto.html', {'form': form, 'total': total, 'carrito': carrito})

def presupuesto_exitoso(request):
    return render(request, 'presupuesto_exitoso.html')

def generar_calendario():
    # Activa el idioma español
    activate('es')

    # Genera el calendario anual
    calendario = {}
    for mes in range(1, 13):
        nombre_mes = format_date(datetime(2024, mes, 1), "MMMM", locale='es')
        dias_mes = calendar.monthcalendar(date.today().year, mes)
        days = []
        for week in dias_mes:
            for dia in week:
                if dia == 0:
                    continue
                try:
                    fecha = datetime(date.today().year, mes, dia)
                except ValueError:
                    continue

                estado = "disponible" if fecha.weekday() in [0, 1, 2] else "ocupado"
                days.append({"fecha": fecha, "estado": estado})
        
        calendario[nombre_mes.capitalize()] = days

    return calendario

def calendario_anual(request):
    calendario = generar_calendario()
    context = {'calendario': calendario}
    return render(request, 'calendario.html', context)
