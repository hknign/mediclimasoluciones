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
from appWeb.views import  register_view, login_view,index_view, productos,servicios,sobre_nosotros,contacto
from appWeb.views import agregar_producto, editar_producto,enviar_presupuesto,pagina_de_confirmacion
from django.contrib.auth.views import LogoutView
from appWeb.views import prueba, ProductoCreateView, eliminar_producto, admin_dashboard, user_dashboard, editar_producto
from appWeb.views import calendario_admin, calendario_usuario, editar_disponibilidad, eliminar_disponibilidad
from django.conf.urls.static import static
from django.conf import settings
from appWeb.views import finalizar_compra,carrito_view,add_to_cart, decrement_from_cart, remove_from_cart, view_cart
from appWeb.views import logout_view, ServicioCreateView, eliminar_servicio,get_total_price_view
from appWeb.views import dias_disponibles,get_product_total_view, editar_servicio

from appWeb.views import editar_sobre_nosotros,preguntas_frecuentes,descargas_view
    




urlpatterns = [
    path('Registro/', register_view,name='Registro'),
    path('', login_view, name='Login'),
    
    path('logout/', logout_view, name='logout'),
    path('index',index_view, name='index'),

    path('productos/', productos, name='productos'),
    path('servicios/', servicios, name='servicios'),

    path('sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', contacto, name='contacto'),

    path('confirmacion/', pagina_de_confirmacion, name='pagina_de_confirmacion'),

    path('finalizar_compra/',finalizar_compra,name='finalizar_compra'),

    path('enviar_presupuesto/', enviar_presupuesto, name='enviar_presupuesto'),

    path('calendario/usuario/', calendario_usuario, name='calendario_usuario'),
    path('calendario/admin/', calendario_admin, name='calendario_admin'),

    path('agregar-producto/', ProductoCreateView.as_view(), name='agregar_producto'),
    path('editar_producto/', editar_producto, name='editar_producto'),

    path('editar_producto/<int:id>/', editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/',eliminar_producto,name='eliminar_producto'),

    path('agregar_servicio/', ServicioCreateView.as_view(), name='agregar_servicio'),
    path('eliminar_servicio/<int:id>/',eliminar_servicio,name='eliminar_servicio'),

    path('prueba/',prueba, name='prueba'),
    path('admin-dashboard/',admin_dashboard, name='admin_dashboard'),

    path('user-dashboard/',user_dashboard, name='user_dashboard'),
    path('editar_disponibilidad/<str:fecha>/', editar_disponibilidad, name='editar_disponibilidad'),

    path('eliminar_disponibilidad/',eliminar_disponibilidad,name='eliminar_disponibilidad'),
    path('carrito/',carrito_view,name='carrito'),

    
    
    path('editar_sobre_nosotros/', editar_sobre_nosotros, name='editar_sobre_nosotros'),
    path('preguntas_frecuentes/', preguntas_frecuentes, name='preguntas_frecuentes'),

    path('descargas/',descargas_view,name='descargas'),

    path('editar_servicio/<int:servicio_id>/', editar_servicio, name='editar_servicio'),
  

    path('add/<int:item_id>/<str:item_type>/', add_to_cart, name='add_to_cart'),
    path('decrement/<int:item_id>/<str:item_type>/', decrement_from_cart, name='decrement_from_cart'),
    path('remove/<int:item_id>/<str:item_type>/', remove_from_cart, name='remove_from_cart'),
    path('view_cart/', view_cart, name='view_cart'),




    path('get_product_total/<int:item_id>/<str:item_type>/', get_product_total_view, name='get_product_total_view'),
 



    path('get_total_price_view/',get_total_price_view,name='get_total_price_view'),
    path('dias_disponibles/',dias_disponibles, name='dias_disponibles'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
