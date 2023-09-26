from django.shortcuts            import render
#from django.http               import HttpResponse
from django.core.files.storage   import default_storage
from django.contrib.auth         import authenticate, login
from django.views.generic.detail import DetailView
from django.views.generic.edit   import UpdateView

from AppFinal.models  import *
from AppFinal.forms   import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def inicio(request):
    try:
        dato = Cliente.objects.get(usuario=request.user.id)
        return render(request, "inicio/inicio.html", {"editaruser": dato.dni, "url": dato.avatar.url})
    except:    
        return render(request, "inicio/inicio.html")

def contacto(request):
    return render(request, "contacto/contacto.html",)

def iniciovendedor(request):
    return render(request, "vendedores/inicio.html",)

# def hola(request):
#     return render(request, "contacto/hola.html",)

# def clientes(request):
#     return render(request, "clientes/inicio.html",)

# def proveedores(request):
#     return render(request, "proveedores/inicio.html",)

# def productos(request):
#     return render(request, "productos/inicio.html",)

# def rubros(request):
#     return render(request, "rubros/inicio.html",)

# def pedidos(request):
#     return render(request, "pedidos/inicio.html",)

#  ---- CLIENTES ---- 
def AltaClienteForm(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        avatar_path = default_storage.save('fotos/clientes'+avatar.name, avatar)
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
            
        else:
                        
            return render(request, "clientes/bienvenido.html",{"mensaje": "Formulario Invalido"})  
    
    else:
        nuevoCliente = Cliente()
        nuevoUsuario = UserCreationForm()
        provincias   = Provincia.objects.all()
    #return render(request, "clientes/alta.html")  
    #return render(request, "clientes/alta.html",{"NewClient": nuevoCliente, "NewUser": nuevoUsuario})  
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
            
            print(loginform.has_error('username'))
            print(loginform.has_error('password'))
            print(loginform.is_valid())
            #print(userok)
            
            editar = Cliente.objects.get(usuario=userok)
            return render(request, "clientes/bienvenido.html",{"mensaje": f'Algo Incorrecto', "saludo": editar.nombre})  
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

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
def AltaVendedorForm(request):
    if request.method == 'POST':
        
        nuevoVendedor = AltaCliente({
                                "nombre": request.POST['nombre'],
                                "dni": request.POST['dni'],
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
        nuevoCliente = Cliente()
        nuevoUsuario = UserCreationForm()
        provincias   = Provincia.objects.all()
    #return render(request, "clientes/alta.html")  
    #return render(request, "clientes/alta.html",{"NewClient": nuevoCliente, "NewUser": nuevoUsuario})  
    return render(request, "clientes/alta.html",{"Pcia": provincias})  

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
                
                return render(request, "clientes/hola.html",{"mensaje": f'Bienvenido/a {editar.nombre}', "paraeditar": editar.cuit})  
            else:
                return render(request, "clientes/hola.html",{"mensaje": f'Login Incorrecto'})  
        else:    
            
            print(loginform.has_error('username'))
            print(loginform.has_error('password'))
            print(loginform.is_valid())
            #print(userok)
            
            editar = Vendedor.objects.get(usuario=userok)
            return render(request, "clientes/bienvenido.html",{"mensaje": f'Algo Incorrecto', "saludo": editar.nombre})  
    else:
        loginform = AuthenticationForm()
        return render(request, "clientes/login.html", {'LoginForm': loginform})

# def DetalleProductoForm(request):
#     detalle = Producto.objects.get(request)
#     return render(request, 'producto/detalle.html', {'detalle_productos': detalle})    


# def ListaPedidosForm(request):
#     lista = OrdenCompra.objects.all()
#     return render(request, 'pedidos/lista.html', {'lista_pedidos': lista})




# def XAltaClienteForm(request):
#     if request.method == 'POST':
#         miForm = AltaCliente(request.POST)
#         if miForm.is_valid():
            
#             info = miForm.cleaned_data
#             nuevoCliente = Cliente(nombre=info['nombre'],
#                                    apellido=info['apellido'],
#                                    dni=info['dni'],
#                                    fnasc=info['fnasc'],
#                                    email=info['email'],
#                                    user=info['user'],
#                                    avatar=info['avatar'],
#                                    domicilio=info['domicilio'],
#                                    provincia=info['provincia'],
#                                    )
#             nuevoCliente.save()
#             return render(request, "clientes/inicio.html",{"mensaje": "Nuevo Cliente CREADO Exitosamente"})  
            
#         else:
#             return render(request, "clientes/inicio.html",{"mensaje": "Formulario Invalido"})  
    
#     else:
#         miForm = AltaCliente()
    
#     return render(request, "clientes/alta.html",{"MiForm": miForm})  

# ##-------------------------------------------------------------------------------------------
# def AltaProveedorForm(request):
#     if request.method == 'POST':
#         miForm = AltaProveedor(request.POST)
#         if miForm.is_valid():
            
#             info = miForm.cleaned_data
#             nuevoProveedor = Proveedor(nombre=info['nombre'],
#                                    contacto=info['contacto'],
#                                    email=info['email'],
#                                    cuit=info['cuit'],
#                                    )
#             nuevoProveedor.save()
#             return render(request, "proveedores/inicio.html",{"mensaje": "Nuevo Proveedor CREADO Exitosamente"})  
            
#         else:
#             return render(request, "proveedores/inicio.html",{"mensaje": "Formulario Invalido"})  
    
#     else:
#         miForm = AltaProveedor()
    
#     return render(request, "proveedores/alta.html",{"MiForm": miForm})  

# ##-------------------------------------------------------------------------------------------
# def AltaProductoForm(request):
#     if request.method == 'POST':
#         miForm = AltaProducto(request.POST)
#         if miForm.is_valid():
            
#             info = miForm.cleaned_data
#             nuevoProducto = Producto(nombre=info['nombre'],
#                                    rubro=info['rubro'],
#                                    precio=info['precio'],
#                                    )
#             nuevoProducto.save()
#             return render(request, "productos/inicio.html",{"mensaje": "Nuevo Producto CREADO Exitosamente"})  
            
#         else:
#             return render(request, "productos/inicio.html",{"mensaje": "Formulario Invalido"})  
    
#     else:
#         miForm = AltaProducto()
    
#     return render(request, "productos/alta.html",{"MiForm": miForm})  

# ##-------------------------------------------------------------------------------------------
# def AltaRubroForm(request):
#     if request.method == 'POST':
#         miForm = AltaRubro(request.POST)
#         if miForm.is_valid():
            
#             info = miForm.cleaned_data
#             nuevoRubro = RubroProd(nombre=info['nombre'],
#                                    )
#             nuevoRubro.save()
#             return render(request, "rubros/inicio.html",{"mensaje": "Nuevo Rubro CREADO Exitosamente"})  
            
#         else:
#             return render(request, "rubros/inicio.html",{"mensaje": "Formulario Invalido"})  
    
#     else:
#         miForm = AltaRubro()
    
#     return render(request, "rubros/alta.html",{"MiForm": miForm})  

# ##-------------------------------------------------------------------------------------------
# def AltaPedidoForm(request):
#     if request.method == 'POST':
#         miForm = AltaPedido(request.POST)
#         if miForm.is_valid():
            
#             info = miForm.cleaned_data
#             nuevoPedido = OrdenCompra(clientes=info['cliente'],
#                                       producto=info['producto'],
#                                       cantidad=info['cantidad'],
#                                    )
#             nuevoPedido.save()
#             return render(request, "pedidos/inicio.html",{"mensaje": "Nuevo Pedido CREADO Exitosamente"})  
            
#         else:
#             return render(request, "pedidos/inicio.html",{"mensaje": "Pedido Invalido"})  
    
#     else:
#         miForm = AltaPedido()
    
#     return render(request, "pedidos/alta.html",{"MiForm": miForm})  





# ## -- BUSQUEDAS -- ##
# def BuscaClienteForm(request):
#     return render(request, "clientes/busca.html")


# def BuscaClienteResultForm(request):
#     if request.GET["dni"]:
#         dni      = request.GET["dni"]  
#         nombre = Cliente.objects.get(dni=dni)
#         if nombre:  
#             return render(request, "clientes/result.html", {"A": nombre})
#         else:
#             return render( "clientes/result.html", {"mensaje": 'No existe ese Cliente'})
#     else:
#         return HttpResponse(f'No existe ese Cliente')
# #------------------------------------------------------------------------------------------------
# def BuscaProveedorForm(request):
#     return render(request, "proveedores/busca.html")


# def BuscaProveedorResultForm(request):
#     if request.GET["cuit"]:
#         cuit      = request.GET["cuit"]  
#         nombre    = Proveedor.objects.get(cuit=cuit)
#         if nombre:  
#             return render(request, "proveedores/result.html", {"A": nombre})
#         else:
#             return render( "proveedores/result.html", {"mensaje": 'No existe ese Proveedor'})
#     else:
#         return HttpResponse(f'No existe ese Proveedor')
# #------------------------------------------------------------------------------------------------
# def BuscaProductoForm(request):
#     return render(request, "productos/busca.html")


# def BuscaProductoResultForm(request):
#     if request.GET["nombre"]:
#         nombre      = request.GET["nombre"]  
#         proveedor    = Producto.objects.get(nombre=nombre)
#         if proveedor:  
#             return render(request, "productos/result.html", {"A": proveedor})
#         else:
#             return render( "productos/result.html", {"mensaje": 'No existe ese Producto'})
#     else:
#         return HttpResponse(f'No existe ese Producto')




# ## -- LISTADOS -- ##

# def ListaClientesForm(request):
#     lista = Cliente.objects.all()
#     return render(request, 'clientes/lista.html', {'lista_clientes': lista})

# def ListaProveedoresForm(request):
#     lista = Proveedor.objects.all()
#     return render(request, 'proveedores/lista.html', {'lista_proveedores': lista})
