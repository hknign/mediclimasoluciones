# Generated by Django 5.1 on 2024-11-09 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0003_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=80),
        ),
    ]