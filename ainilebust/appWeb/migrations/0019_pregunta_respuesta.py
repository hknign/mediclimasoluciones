# Generated by Django 5.1 on 2024-11-27 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0018_rename_pregunta_pregunta_contenido_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='respuesta',
            field=models.TextField(blank=True, null=True),
        ),
    ]