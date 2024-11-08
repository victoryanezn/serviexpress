from django.contrib import admin
from django.urls import path
from . import views
from serviexpress import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('servicio/', views.servicio, name='servicio'),
    path('servicio/crear/', views.crear_servicio, name='crear_servicio'),
    path('servicio/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    path('servicio/<int:servicio_id>/eliminar', views.eliminar_servicio, name='eliminar_servicio'),



    path('proveedor/', views.proveedor, name='proveedor'),
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/<int:proveedor_id>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('proveedor/<int:proveedor_id>/eliminar', views.eliminar_proveedor, name='eliminar_proveedor'),

    path('proveedores/', views.proveedorMec, name='proveedores'),
    # path('promocion/', views.promocion, name='promocion'),
    # path('promocion/crear/', views.crear_promocion, name='crear_promocion'),
    # path('promocion/<str:promocion_id>/', views.detalle_promocion, name='detalle_promocion'),
    # path('promocion/<str:promocion_id>/eliminar', views.eliminar_promocion, name='eliminar_promocion'),
    # path('servicioCl/', views.servicioCl, name='servicioCl'),
    path('cotizaciones/', views.cotizacionCl, name='cotizacionCl'),
    path('quienes-somos/', views.quienesSomos, name='QuienesSomos'),
    path('carrito/', views.carrito, name="carrito"),
    path('agregar/<int:servicio_id>/', views.agregar_carro, name="Add"),
    path('servicios/agregar/<int:servicio_id>/', views.agregar_carro_servicios, name="serviciosAdd"),
    path('eliminar/<int:servicio_id>/', views.eliminar_carro, name="Del"),
    path('restar/<int:servicio_id>/', views.restar_carro, name="Sub"),
    path('limpiar/', views.limpiar_carro, name="Clean"),
]