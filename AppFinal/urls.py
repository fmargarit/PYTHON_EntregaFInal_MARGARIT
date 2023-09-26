from django.urls import path
from django.contrib.auth.views import LogoutView
from AppFinal.views import *


urlpatterns = [
    
    path('inicio/', inicio, name='InicioURL'),
    path('', inicio, name='InicioURL'),
    
    path('contacto', contacto, name='ContactoURL'),
    
    path('clientes/alta/',       AltaClienteForm,  name='ClientesAltaURL'),
    path('clientes/login',       LoginClienteForm, name='ClientesLoginURL'),
    #path('clientes/hola/<pk>',   Hola.as_view(template_name='clientes/hola.html'), name='HolaURL'),
    path('clientes/editar/<pk>', ClienteUpdateView.as_view(), name='ClientesEditarURL'),
    path('clientes/logout/',     LogoutView.as_view(template_name='inicio/inicio.html'), name='ClientesLogoutURL'),

    path('producto/detalle/<pk>', DetalleProductoForm.as_view(), name='ProductosDetalleURL'),
    path('producto/lista/<int:start>', ListaProductosForm, name='ProductosListaURL'),
    
    path('vendedores/inicio/',     iniciovendedor,    name='VendedoresInicioURL'),
    path('vendedores/alta/',       AltaVendedorForm,  name='VendedoresAltaURL'),
    path('vendedores/login',       LoginVendedorForm, name='VendedoresLoginURL'),
    path('vendedores/editar/<pk>', VendedorUpdateView.as_view(), name='VendedoresEditarURL'),
    path('vendedores/logout/',     LogoutView.as_view(template_name='vendedores/inicio.html'), name='VendedoresLogoutURL'),

    path('productos/alta/',        AltaProductoForm,  name='ProductosAltaURL'),
]