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
    path('vendedores/logout/',     LogoutView.as_view(template_name='vendedores/inicio.html'), name='VendedoresLogoutURL'),

    
#     path('clientes/busca/', BuscaClienteForm, name='ClientesBuscaURL'),
#     path('clientes/result/', BuscaClienteResultForm, name='ClientesBuscaResultURL'),
#     path('clientes/lista/', ListaClientesForm, name='ClientesListaURL'),
    
    
#     path('proveedores/', proveedores, name='ProveedoresURL'),
#     path('proveedores/alta/', AltaProveedorForm, name='ProveedorAltaURL'),
#     path('proveedores/busca/', BuscaProveedorForm, name='ProveedoresBuscaURL'),
#     path('proveedores/result/', BuscaProveedorResultForm, name='ProveedoresBuscaResultURL'),
#     path('proveedores/lista/', ListaProveedoresForm, name='ProveedoresListaURL'),
    
    
#     path('producto/', productos, name='ProductosURL'),
#     path('producto/alta/', AltaProductoForm, name='ProductoAltaURL'),
#     path('producto/busca/', BuscaProductoForm, name='ProductosBuscaURL'),
      
#     path('rubro/', rubros, name='RubrosURL'),
#     path('rubro/alta/', AltaRubroForm, name='RubroAltaURL'),
#     path('rubro/lista/', ListaRubrosForm, name='RubrosListaURL'),
    
#     path('pedidos/', pedidos, name='PedidosURL'),
#     path('pedidos/alta/', AltaPedidoForm, name='PedidoAltaURL'),
#     path('pedidos/lista/', ListaPedidosForm, name='PedidosListaURL'),
]