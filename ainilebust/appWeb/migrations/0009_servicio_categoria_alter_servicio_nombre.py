# Generated by Django 5.1 on 2024-11-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0008_remove_itemcarrito_usuario_alter_carrito_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='categoria',
            field=models.CharField(choices=[('INSTALACION', 'Instalación'), ('MANTENIMIENTO', 'Mantenimiento'), ('SOPORTE_TECNICO', 'Soporte Técnico')], default='INSTALACION', max_length=50),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]