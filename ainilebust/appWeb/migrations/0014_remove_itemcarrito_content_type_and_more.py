# Generated by Django 5.1 on 2024-11-22 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0013_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcarrito',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='itemcarrito',
            name='object_id',
        ),
    ]
