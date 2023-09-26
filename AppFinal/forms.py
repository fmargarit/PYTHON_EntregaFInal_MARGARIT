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
        fields = ('rubro','marca','nombre','precio','stock','foto','detalle')
 
 # class AltaCliente(forms.Form):
#     nombre   = forms.CharField(required=True)
#     apellido = forms.CharField(required=True)
#     dni      = forms.IntegerField(required=True)
#     fnasc    = forms.DateField(required=True)
#     email    = forms.EmailField(required=True)
#     usuario  = forms.EmailField(required=True)
#     avatar   = forms.ImageField(required=False)
#     domicilio= forms.CharField(required=True)
#     provincia= forms.ModelChoiceField(queryset=Provincia.objects.all(), to_field_name=Cliente.provincia)
    

 
         
# class AltaProveedor(forms.Form):
#     nombre   = forms.CharField(required=True)
#     contacto = forms.CharField(required=True)
#     email    = forms.EmailField(required=True)
#     cuit     = forms.IntegerField(required=True)

# class AltaRubro(forms.Form):
#     nombre   = forms.CharField(required=True)
    
# class AltaProducto(forms.Form):
#     nombre   = forms.CharField(required=True)
#     proveedor= forms.ChoiceField(widget=forms.Select(choices=Proveedor.objects.all()))
#     rubro    = forms.ChoiceField(widget=forms.Select(choices=RubroProd.objects.all()))
#     precio   = forms.DecimalField(required=True)
    
# class AltaPedido(forms.Form):
#     comprador= forms.CharField(required=True)
#     producto = forms.CharField(required=True)
#     cantidad = forms.DecimalField(required=True)