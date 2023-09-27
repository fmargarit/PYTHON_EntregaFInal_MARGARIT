from django.shortcuts            import render
#from django.http               import HttpResponse
from django.core.files.storage   import default_storage
from django.contrib.auth         import authenticate, login
from django.views.generic.detail import DetailView
from django.views.generic.edit   import UpdateView

from AppFinal.models  import *
from AppFinal.forms   import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LogoutView

# Create your views here.
# ----------------------------------------------------------------------------------------------------------------
def inicio(request):
    try:
        dato = Cliente.objects.get(usuario=request.user.id)
        return render(request, "inicio/inicio.html", {"editaruser": dato.dni, "url": dato.avatar.url})
    except:    
        logoutuser = LogoutView.as_view(template_name='inicio/inicio.html')
        return logoutuser(request)

# ----------------------------------------------------------------------------------------------------------------
def contacto(request):
    return render(request, "contacto/contacto.html",)

# ----------------------------------------------------------------------------------------------------------------
def iniciovendedor(request):
    try:
        dato = Vendedor.objects.get(usuario=request.user.id)
        return render(request, "vendedores/inicio.html", {"editarvendedor": dato.cuit})
    except:    
        logoutuser = LogoutView.as_view(template_name='vendedores/inicio.html')
        return logoutuser(request)
    
# ----------------------------------------------------------------------------------------------------------------
def CompraProductoForm(request):
    return render(request, "compra/fondo.html",)

# ----------------------------------------------------------------------------------------------------------------
def AltaClienteForm(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        
        if avatar is None:
            avatar_path = 'fotos/clientes/emoji.jpg'
        else:
            avatar_path = default_storage.save('fotos/clientes/'+avatar.name, avatar)
            
        nuevoCliente = AltaCliente({
                                "nombre": request.POST['nombre'],
                                "apellido": request.POST['apellido'],
                                "dni": request.POST['dni'],
                                "fnac": request.POST['fnac'],
                                "email": request.POST['email'],
                                "avatar": avatar_path,
                                "domicilio": request.POST['domicilio'],
                                "provincia": request.POST['provincia'],
                                })
       
        nuevoUsuario = UserCreationForm({
                                "username": request.POST["username"],
                                "password1": request.POST["password1"],
                                "password2": request.POST["password2"]
                                })
                
        if nuevoCliente.is_valid() and nuevoUsuario.is_valid():
            
            data = nuevoCliente.cleaned_data
            data.update(nuevoUsuario.cleaned_data)
            
            usuario = User(username=data['username'])
            usuario.set_password(data['password1'])
            usuario.save()
            
            client = Cliente(nombre=data['nombre'],
                            apellido=data['apellido'],
                            dni=data['dni'],
                            fnac=data['fnac'],
                            email=data['email'],
                            avatar=avatar_path,
                            domicilio=data['domicilio'],
                            provincia=data['provincia'],
                            usuario=usuario
                            )
            client.save()
            return render(request, "clientes/bienvenido.html",{"mensaje1": f'Usuario Registrado con exito', "mensaje2": f'Ingrese al sistema'})  
        
        elif nuevoUsuario.is_valid() == False:
        
            return render(request, "clientes/bienvenido.html",{"mensaje1": "Contraseñas Difieren"})  
        
        else:
            
            print(nuevoCliente.is_valid())
            print(nuevoUsuario.is_valid())
            print(nuevoCliente.has_error('nombre'))
            print(nuevoCliente.has_error('apellido'))
            print(nuevoCliente.has_error('fnac'))
            print(nuevoCliente.has_error('avatar'))
                        
            return render(request, "clientes/bienvenido.html",{"mensaje1": "Formulario Invalido"})  
    
    else:
        nuevoCliente = Cliente()
        nuevoUsuario = UserCreationForm()
        provincias   = Provincia.objects.all()
    return render(request, "clientes/alta.html",{"Pcia": provincias})  

# ----------------------------------------------------------------------------------------------------------------
def LoginClienteForm(request):
    if request.method == 'POST':
        loginform = AuthenticationForm(request, data=request.POST)
        
        if loginform.is_valid():
            data   = loginform.cleaned_data
            user   = data['username']
            psw    = data['password']
                        
            userok = authenticate(username=user, password=psw)
            
            editar = Cliente.objects.get(usuario=userok)
            
            if userok:
                login(request, userok)                
                return render(request, "clientes/hola.html",{"mensaje": f'Bienvenido/a {editar.nombre}', "paraeditar": editar.dni})  
            
            else:
                return render(request, "clientes/hola.html",{"mensaje": f'Login Incorrecto'})  
        else:    
                      
            return render(request, "clientes/bienvenido.html",{"mensaje1": f'Algo Incorrecto', "mensaje2": f' Usuario y/o Contraseña Incorrectos'})  
    else:
        loginform = AuthenticationForm()
        return render(request, "clientes/login.html", {'LoginForm': loginform})

# ----------------------------------------------------------------------------------------------------------------
def ListaProductosForm(request, start=1):
        
    cantreg  = Producto.objects.all().count()
    cantxpag = 3
    if (cantreg % cantxpag) == 0:
        maxpag   = (cantreg // cantxpag)
    else:
        maxpag   = (cantreg // cantxpag) + 1
            
    if request.GET.get('direction') == 'proximo':
        if start < maxpag:
            start +=1
        
    elif request.GET.get('direction') == 'anterior':
        if start == 1:
            start = 1
        else:
            start -=1
                
    inicio = (int(start)-1) * cantxpag 
    final  = inicio + 3
    lista  = Producto.objects.all()[inicio:final]
    
    try:
        foto = Cliente.objects.get(usuario=request.user.id)
        return render(request, "productos/lista.html", {"lista_productos": lista, "pagina": start, "url": foto.avatar.url})
    except:  
    
        return render(request, 'productos/lista.html', {"lista_productos": lista, "pagina": start})
   
# ----------------------------------------------------------------------------------------------------------------
class DetalleProductoForm(DetailView):
    model               = Producto
    template_name       = 'productos/detalle.html'
    context_object_name = 'detalle'

class Hola(DetailView):
    model               = User
    template_name       = 'clientes/hola.html'
    context_object_name = 'hola'
    
class ClienteUpdateView(UpdateView):
    model               = Cliente
    template_name       = 'clientes/editar.html'        
    fields              = ('nombre','apellido','dni','fnac','email','avatar','domicilio','provincia')
    success_url         = '/entregable/'
    context_object_name = 'edit'
    
class VendedorUpdateView(UpdateView):
    model               = Vendedor
    template_name       = 'vendedores/editar.html'        
    fields              = ('nombre','cuit','email','domicilio','provincia')
    success_url         = '/entregable/vendedores/inicio'
    context_object_name = 'edit'

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
def AltaVendedorForm(request):
    if request.method == 'POST':
        nuevoVendedor = AltaVendedor({
                                "nombre": request.POST['nombre'],
                                "cuit": request.POST['cuit'],
                                "email": request.POST['email'],
                                "domicilio": request.POST['domicilio'],
                                "provincia": request.POST['provincia'],
                                })

        nuevoUsuario = UserCreationForm({
                                "username": request.POST["username"],
                                "password1": request.POST["password1"],
                                "password2": request.POST["password2"]
                                })
                
        if nuevoVendedor.is_valid() and nuevoUsuario.is_valid():
            
            data = nuevoVendedor.cleaned_data
            data.update(nuevoUsuario.cleaned_data)
            
            usuario = User(username=data['username'])
            usuario.set_password(data['password1'])
            usuario.save()
            
            vended = Vendedor(nombre=data['nombre'],
                            cuit=data['cuit'],
                            email=data['email'],
                            domicilio=data['domicilio'],
                            provincia=data['provincia'],
                            usuario=usuario
                            )
            vended.save()
            return render(request, "vendedores/bienvenido.html",{"mensaje1": f'Vendedor Registrado con exito', "mensaje2": f'Ingrese al sistema'})  
            
        else:
                        
            return render(request, "vendedores/bienvenido.html",{"mensaje": "Formulario Invalido"})  
    
    else:
        nuevoVendedor = Vendedor()
        nuevoUsuario  = UserCreationForm()
        provincias    = Provincia.objects.all()
    
    return render(request, "vendedores/alta.html",{"Pcia": provincias})  

# ----------------------------------------------------------------------------------------------------------------
def LoginVendedorForm(request):
    if request.method == 'POST':
        loginform = AuthenticationForm(request, data=request.POST)
        
        if loginform.is_valid():
            data   = loginform.cleaned_data
            user   = data['username']
            psw    = data['password']
                        
            userok = authenticate(username=user, password=psw)
            
            editar = Vendedor.objects.get(usuario=userok)
            
            if userok:
                login(request, userok)
                
                return render(request, "vendedores/hola.html",{"mensaje": f'Bienvenido/a {editar.nombre}', "editarvendedor": editar.cuit})  
            else:
                return render(request, "vendedores/hola.html",{"mensaje": f'Login Incorrecto'})  
        else:    
            
            print(loginform.has_error('username'))
            print(loginform.has_error('password'))
            print(loginform.is_valid())
                                   
            return render(request, "vendedores/bienvenido.html",{"mensaje1": f'Algo Incorrecto', "mensaje2": f' Usuario y/o Contraseña Incorrectos'})  
    else:
        loginform = AuthenticationForm()
        return render(request, "vendedores/login.html", {'LoginForm': loginform})

# ----------------------------------------------------------------------------------------------------------------
def AltaProductoForm(request):
    if request.method == 'POST':
        imagen = request.FILES.get('foto')
        imagen_path = default_storage.save('fotos/productos/'+imagen.name, imagen)  
        nuevoProducto = AltaProducto({
                                "marca":   request.POST['marca'],
                                "rubro":   request.POST['rubro'],
                                "nombre":  request.POST['nombre'],
                                "precio":  request.POST['precio'],
                                "stock":   request.POST['stock'],
                                "detalle": request.POST['detalle'],
                                "foto":    imagen_path
                                })

        if nuevoProducto.is_valid():
            
            data = nuevoProducto.cleaned_data
            
            produ = Producto(rubro=data['rubro'],
                             marca=data['marca'],
                             nombre=data['nombre'],
                             precio=data['precio'],
                             stock=data['stock'],
                             detalle=data['detalle'],
                             foto=imagen_path
                            )
            produ.save()
            
            return render(request, "productos/bienvenido.html",{"mensaje": f'Producto Registrado con exito'})  
        else:
                        
            return render(request, "productos/bienvenido.html",{"mensaje": "Formulario Invalido"})  
    else:
        nuevoProducto = Producto()
        marcas     = MarcaProd.objects.all()
        rubros     = RubroProd.objects.all()
        
    return render(request, "productos/alta.html",{"Marc": marcas, "Rubr": rubros})  