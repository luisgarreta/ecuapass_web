# Generated by Django 5.0 on 2024-01-19 00:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creador', '0004_rename_direcccion_empresa_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartaporte',
            name='fecha_emision',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
