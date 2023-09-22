
from django.db import models
from django.contrib.auth.models import User

#-------------------------------------------------------------------------------------
class Provincia(models.Model):
    provincia   = models.CharField(primary_key=True, max_length=30)
    def __str__(self):
        return f'{self.provincia}'
    class Meta():
        verbose_name = 'PROVINCIA'
        verbose_name_plural = 'PROVINCIA'

#-------------------------------------------------------------------------------------
class Cliente(models.Model):
    nombre   = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni      = models.IntegerField(primary_key=True)
    fnac     = models.DateField(null=False)
    email    = models.EmailField(null=False)
    usuario  = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar   = models.ImageField(upload_to='fotos/clientes', blank=True, null=True)
    domicilio= models.CharField(max_length=150)
    provincia= models.ForeignKey(Provincia, on_delete=models.DO_NOTHING)
    cliente  = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    class Meta():
        verbose_name = 'CLIENTE'
        verbose_name_plural = 'CLIENTES'
    
#-------------------------------------------------------------------------------------
class RubroProd(models.Model):
    rubro   = models.CharField(primary_key=True, max_length=30)
    def __str__(self):
        return f'{self.rubro}'
    class Meta():
        verbose_name = 'RUBRO'
        verbose_name_plural = 'RUBROS'

#-------------------------------------------------------------------------------------
class MarcaProd(models.Model):
    marca   = models.CharField(primary_key=True, max_length=30)
    def __str__(self):
        return f'{self.marca}'
    class Meta():
        verbose_name = 'MARCA'
        verbose_name_plural = 'MARCA'
        
#-------------------------------------------------------------------------------------
class Producto(models.Model):
    rubro    = models.ForeignKey(RubroProd, on_delete=models.DO_NOTHING)
    marca    = models.ForeignKey(MarcaProd, on_delete=models.DO_NOTHING)
    nombre   = models.CharField(max_length=30)
    precio   = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    stock    = models.IntegerField(default=0)
    foto     = models.ImageField(upload_to='fotos/productos', blank=True, null=True)
    detalle  = models.TextField(max_length=255)
    def __str__(self):
        return f'{self.nombre}'
    class Meta():
        verbose_name = 'PRODUCTO'
        verbose_name_plural = 'PRODUCTOS'

#-------------------------------------------------------------------------------------
class OrdenCompra(models.Model):
    comprador = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    producto  = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad  = models.DecimalField(decimal_places=0, max_digits=20, default=1)
    class Meta():
        verbose_name = 'ORDEN COMPRA'
        verbose_name_plural = 'ORDENES COMPRA'