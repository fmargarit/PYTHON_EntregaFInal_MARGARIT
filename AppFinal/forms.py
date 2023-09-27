from django import forms
from AppFinal.models import Cliente, Vendedor, Producto, Provincia, MarcaProd, RubroProd


class AltaCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre','apellido','dni','fnac','email','avatar','domicilio','provincia')
        
class AltaVendedor(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ('nombre','cuit','email','domicilio','provincia')
        
class AltaProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('rubro','marca','nombre','precio','stock','detalle', 'foto')
 