from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .Carrito import Carrito 
from .forms import ServicioForm, PromocionForm, ProveedorForm, ProveedorFilterForm
from .models import Servicio, Promocion, TipoServicio, TipoProveedor, Proveedor
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
import os 

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm()
        })
        
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                        password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', { 
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html',{
                        'form': UserCreationForm,
                        "error": 'Las contraseñas no coinciden'
                    })

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password = request.POST
                ['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'El nombre o la contraseña es incorrecto'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def crear_servicio(request):
    if request.method == 'GET':
        return render(request, 'crear_servicio.html', {
            'form': ServicioForm
        })
    else:
        try:
            form = ServicioForm(request.POST, request.FILES)
            imagen_nueva = request.FILES['imagen']
            if imagen_nueva:
                new_servicio = form.save(commit=False)
                # Verifica si la imagen ya existe en la carpeta media
                imagen_path = os.path.join(settings.MEDIA_ROOT, 'servicios', imagen_nueva.name)
                if os.path.exists(imagen_path):
                    # La imagen ya existe, Se asigna el path de la imagen existente
                    new_servicio.imagen = os.path.join('servicios', imagen_nueva.name)
                else:
                    # La imagen no existe, guardamos la nueva imagen con su respectivo path
                    new_servicio.imagen = imagen_nueva
            new_servicio.save()
            return redirect('servicio')
        except ValueError:
            return render(request, 'crear_servicio.html', {
            'form': ServicioForm,
            'error': 'Porfavor provee datos validos'
            })

@login_required
def servicio(request):
    if not request.user.is_staff:
        return redirect('home')
    else:
        servicios = Servicio.objects.all()
        return render(request, 'servicio.html', {'servicios': servicios})

@login_required
def detalle_servicio(request, servicio_id):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'GET':
        servicio = get_object_or_404(Servicio, pk=servicio_id)
        form = ServicioForm(instance=servicio)
        return render(request, 'detalle_servicio.html', {'servicio': servicio, 'form': form})
    else:
        servicio = get_object_or_404(Servicio, pk=servicio_id)
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            imagen_nueva = form.cleaned_data.get('imagen')
            if imagen_nueva:
                # Verifica si la imagen ya existe en la carpeta media
                imagen_path = os.path.join(settings.MEDIA_ROOT, 'servicios', imagen_nueva.name)
                if os.path.exists(imagen_path):
                    # La imagen ya existe, Se asigna el path de la imagen existente
                    servicio.imagen = os.path.join('servicios', imagen_nueva.name)
                else:
                    # La imagen no existe, guardamos la nueva imagen con su respectivo path
                    servicio.imagen = imagen_nueva
            servicio.save()
            return redirect('servicio')
        else:
            return render(request, 'detalle_servicio.html', {'servicio': servicio, 'form': form, 'error': 'Error al actualizar el servicio'})
        
@login_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicio')

@login_required
def crear_promocion(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'crear_promocion.html', {
            'form': PromocionForm
        })
    else:
        try:
            form = PromocionForm(request.POST, request.FILES)
            new_promocion = form.save(commit=False)
            new_promocion.save()
            return redirect('promocion')
        except ValueError:
            return render(request, 'crear_promocion.html', {
            'form': PromocionForm,
            'error': 'Porfavor provee datos validos'
            })
        
@login_required
def promocion(request):
    if not request.user.is_staff:
        return redirect('home')
    else:
        promociones = Promocion.objects.all()
        return render(request, 'promocion.html', {'promociones': promociones})
        
@login_required
def detalle_promocion(request, promocion_id):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'GET':
        promocion = get_object_or_404(Promocion, pk=promocion_id)
        form = PromocionForm(instance=promocion)
        return render(request, 'detalle_promocion.html', {'promocion': promocion, 'form': form})
    else:
        try:
            promocion = get_object_or_404(Promocion, pk=promocion_id)
            form = PromocionForm(request.POST, instance=promocion)
            form.save()
            return redirect('promocion')
        except ValueError:
            return render(request, 'detalle_promocion.html', {'promocion': promocion, 'form': form, 'error': "Error al actualizar la Promocion"})
        
@login_required
def eliminar_promocion(request, promocion_id):
    promocion = get_object_or_404(Promocion, pk=promocion_id)
    if request.method == 'POST':
        promocion.delete()
        return redirect('promocion')
    

# Sin Bucador -------------------------------------------------------------
# def servicioCl(request):
#     servicios = Servicio.objects.filter(estado=1)
#     return render(request, 'servicioCl.html', {'servicios': servicios})

# Con Buscador--------------
def cotizacionCl(request):
    query = request.GET.get('q', '')
    tipo_servicio_id = request.GET.get('tipo_servicio', '')

    servicios = Servicio.objects.filter(estado=1)
    
    if query:
        servicios = servicios.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(tipo_servicio__nombre__icontains=query)
        )

    if tipo_servicio_id:
        servicios = servicios.filter(tipo_servicio_id=tipo_servicio_id)
        
    no_results = not servicios.exists()
    tipos_servicio = TipoServicio.objects.all()
    
    return render(request, 'cotizacionCl.html', {
        'servicios': servicios, 
        'query': query, 
        'no_results': no_results, 
        'tipos_servicio': tipos_servicio,
        'selected_tipo_servicio': tipo_servicio_id
    })



@login_required
def carrito(request):
    servicios = Servicio.objects.all()
    return render(request, 'carrito.html', {'servicios':servicios})

@login_required
def agregar_carro(request, servicio_id):
    carrito = Carrito(request)
    servicio = Servicio.objects.get(id = servicio_id)
    carrito.agregar(servicio)
    return redirect('carrito')

@login_required
def agregar_carro_servicios(request, servicio_id):
    carrito = Carrito(request)
    servicio = Servicio.objects.get(id = servicio_id)
    carrito.agregar(servicio)
    return redirect('cotizacionCl')

@login_required
def eliminar_carro(request, servicio_id):
    carrito = Carrito(request)
    servicio = Servicio.objects.get(id = servicio_id)
    carrito.eliminar(servicio)
    return redirect('carrito')

@login_required
def restar_carro(request, servicio_id):
    carrito = Carrito(request)
    servicio = Servicio.objects.get(id = servicio_id)
    carrito.restar(servicio)
    return redirect('carrito')

@login_required
def limpiar_carro(request):
    carrito = Carrito(request)
    carrito.limpiar_carrito()
    return redirect('carrito')



def quienesSomos(request):
    return render(request, 'quienes_somos.html')



# --------------------------------------------------

@login_required
def crear_proveedor(request):
    if request.method == 'GET':
        return render(request, 'crear_proveedor.html', {
            'form': ProveedorForm()
        })
    else:
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor')
        else:
            return render(request, 'crear_proveedor.html', {
                'form': form,
                'error': 'Por favor, provee datos válidos'
            })

@login_required
def proveedor(request):
    if not request.user.is_staff:
        return redirect('home')
    else:
        proveedores = Proveedor.objects.all()
        return render(request, 'proveedor.html', {'proveedores': proveedores})

@login_required
def detalle_proveedor(request, proveedor_id):
    if not request.user.is_staff:
        return redirect('home')
    
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    
    if request.method == 'GET':
        form = ProveedorForm(instance=proveedor)
        return render(request, 'detalle_proveedor.html', {'proveedor': proveedor, 'form': form})
    else:
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor')
        else:
            return render(request, 'detalle_proveedor.html', {
                'proveedor': proveedor,
                'form': form,
                'error': 'Error al actualizar el proveedor'
            })
        
@login_required
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor')
    
def proveedorMec(request):
    query = request.GET.get('q', '')
    tipo_proveedor_id = request.GET.get('tipo_proveedor', '')

    proveedores = Proveedor.objects.filter()
    
    if query:
        proveedores = proveedores.filter(
            Q(nombre_empresa__icontains=query) | 
            Q(direccion__icontains=query) |
            Q(productos__icontains=query) |
            Q(tipo_proveedor__nombre__icontains=query)
        )

    if tipo_proveedor_id:
        proveedores = proveedores.filter(tipo_proveedor_id=tipo_proveedor_id)

    no_results = not proveedores.exists()
    tipos_proveedor = TipoProveedor.objects.all()
    
    return render(request, 'proveedoresMec.html', {
        'proveedores': proveedores, 
        'query': query, 
        'no_results': no_results, 
        'tipos_proveedor': tipos_proveedor,
        'selected_tipo_proveedor': tipo_proveedor_id
    })