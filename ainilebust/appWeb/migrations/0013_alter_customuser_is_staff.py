# Generated by Django 5.1 on 2024-11-22 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0012_itemcarrito_content_type_itemcarrito_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
