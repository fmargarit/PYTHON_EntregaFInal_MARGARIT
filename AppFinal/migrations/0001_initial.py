# Generated by Django 4.2.4 on 2023-09-20 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('dni', models.IntegerField(primary_key=True, serialize=False)),
                ('fnasc', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatares')),
                ('domicilio', models.CharField(max_length=150)),
                ('cliente', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'CLIENTE',
                'verbose_name_plural': 'CLIENTES',
            },
        ),
        migrations.CreateModel(
            name='MarcaProd',
            fields=[
                ('marca', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'MARCA',
                'verbose_name_plural': 'MARCA',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('provincia', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'PROVINCIA',
                'verbose_name_plural': 'PROVINCIA',
            },
        ),
        migrations.CreateModel(
            name='RubroProd',
            fields=[
                ('rubro', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'RUBRO',
                'verbose_name_plural': 'RUBROS',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('stock', models.IntegerField(default=0)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='avatares')),
                ('detalle', models.TextField(max_length=255)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='AppFinal.marcaprod')),
                ('rubro', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='AppFinal.rubroprod')),
            ],
            options={
                'verbose_name': 'PRODUCTO',
                'verbose_name_plural': 'PRODUCTOS',
            },
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=0, default=1, max_digits=20)),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='AppFinal.cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='AppFinal.producto')),
            ],
            options={
                'verbose_name': 'ORDEN COMPRA',
                'verbose_name_plural': 'ORDENES COMPRA',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='AppFinal.provincia'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]