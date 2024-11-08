"""
URL configuration for ainilebust project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appWeb.views import  register_view, login_view,index_view, productos,servicios,sobre_nosotros,contacto, agregar_al_carrito, eliminar_del_carrito, mostrar_carrito,realizar_presupuesto,presupuesto_exitoso, horarios
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('Registro/', register_view,name='Registro'),
    path('', login_view, name='Login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index',index_view, name='index'),
    path('productos/', productos, name='productos'),
    path('servicios/', servicios, name='servicios'),
    path('sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', contacto, name='contacto'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', mostrar_carrito, name='mostrar_carrito'),
    path('realizar-presupuesto/', realizar_presupuesto, name='realizar_presupuesto'),
    path('presupuesto-exitoso/', presupuesto_exitoso, name='presupuesto_exitoso'),
    path('horarios/',horarios, name='horarios'),



]