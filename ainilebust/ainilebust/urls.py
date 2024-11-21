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
from appWeb.views import  register_view, login_view,index_view, productos,servicios,sobre_nosotros,contacto#, #agregar_al_carrito, eliminar_del_carrito, mostrar_carrito
from appWeb.views import realizar_presupuesto,presupuesto_exitoso, agregar_producto, editar_producto
from django.contrib.auth.views import LogoutView
from appWeb.views import prueba, ProductoCreateView, eliminar_producto, admin_dashboard, user_dashboard, editar_producto
from appWeb.views import calendario_admin, calendario_usuario, editar_disponibilidad, eliminar_disponibilidad
from django.conf.urls.static import static
from django.conf import settings
from appWeb.views import agregar_producto_al_carrito, agregar_servicio_al_carrito,eliminar_item_carrito,ver_carrito, finalizar_compra
from appWeb.views import logout_view
urlpatterns = [
    path('Registro/', register_view,name='Registro'),
    path('', login_view, name='Login'),
    path('logout/', logout_view, name='logout'),
    path('index',index_view, name='index'),
    path('productos/', productos, name='productos'),
    path('servicios/', servicios, name='servicios'),
    path('sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', contacto, name='contacto'),
    path('agregar_producto/<int:producto_id>/',agregar_producto_al_carrito, name='agregar_producto_al_carrito'),
    path('agregar_servicio/<int:servicio_id>/',agregar_servicio_al_carrito, name='agregar_servicio_al_carrito'),
    path('eliminar_item/<int:item_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('finalizar_compra/',finalizar_compra,name='finalizar_compra'),
    path('realizar-presupuesto/', realizar_presupuesto, name='realizar_presupuesto'),
    path('presupuesto-exitoso/', presupuesto_exitoso, name='presupuesto_exitoso'),
    path('calendario/usuario/', calendario_usuario, name='calendario_usuario'),
    path('calendario/admin/', calendario_admin, name='calendario_admin'),
    path('agregar-producto/', ProductoCreateView.as_view(), name='agregar_producto'),
    path('editar_producto/', editar_producto, name='editar_producto'),
    path('editar_producto/<int:id>/', editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/',eliminar_producto,name='eliminar_producto'),
    path('prueba/',prueba, name='prueba'),
    path('admin-dashboard/',admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/',user_dashboard, name='user_dashboard'),
    path('editar_disponibilidad/<str:fecha>/', editar_disponibilidad, name='editar_disponibilidad'),
    path('eliminar_disponibilidad/',eliminar_disponibilidad,name='eliminar_disponibilidad')



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
