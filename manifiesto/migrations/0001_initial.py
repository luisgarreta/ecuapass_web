# Generated by Django 5.0.1 on 2024-01-25 19:28

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ManifiestoDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
                ('txt00', models.CharField(max_length=20)),
                ('txt01', models.CharField(max_length=200)),
                ('txt02', models.CharField(max_length=200)),
                ('txt03', models.CharField(max_length=200)),
                ('txt04', models.CharField(max_length=200)),
                ('txt05', models.CharField(max_length=200)),
                ('txt06', models.CharField(max_length=200)),
                ('txt07', models.CharField(max_length=200)),
                ('txt08', models.CharField(max_length=200)),
                ('txt09', models.CharField(max_length=200)),
                ('txt10', models.CharField(max_length=200)),
                ('txt11', models.CharField(max_length=200)),
                ('txt12', models.CharField(max_length=200)),
                ('txt13', models.CharField(max_length=200)),
                ('txt14', models.CharField(max_length=200)),
                ('txt15', models.CharField(max_length=200)),
                ('txt16', models.CharField(max_length=200)),
                ('txt17', models.CharField(max_length=200)),
                ('txt18', models.CharField(max_length=200)),
                ('txt19', models.CharField(max_length=200)),
                ('txt20', models.CharField(max_length=200)),
                ('txt21', models.CharField(max_length=200)),
                ('txt22', models.CharField(max_length=200)),
                ('txt23', models.CharField(max_length=200)),
                ('txt24', models.CharField(max_length=200)),
                ('txt25_1', models.CharField(max_length=200)),
                ('txt25_2', models.CharField(max_length=200)),
                ('txt25_3', models.CharField(max_length=200)),
                ('txt25_4', models.CharField(max_length=200)),
                ('txt25_5', models.CharField(max_length=200)),
                ('txt26', models.CharField(max_length=200)),
                ('txt27', models.CharField(max_length=200)),
                ('txt28', models.CharField(max_length=200)),
                ('txt29', models.CharField(max_length=200)),
                ('txt30', models.CharField(max_length=200)),
                ('txt31', models.CharField(max_length=200)),
                ('txt32_1', models.CharField(max_length=200)),
                ('txt32_2', models.CharField(max_length=200)),
                ('txt32_3', models.CharField(max_length=200)),
                ('txt32_4', models.CharField(max_length=200)),
                ('txt33_1', models.CharField(max_length=200)),
                ('txt33_2', models.CharField(max_length=200)),
                ('txt34', models.CharField(max_length=200)),
                ('txt35', models.CharField(max_length=200)),
                ('txt36', models.CharField(max_length=200)),
                ('txt37', models.CharField(max_length=200)),
                ('txt38', models.CharField(max_length=200)),
                ('txt39', models.CharField(max_length=200)),
                ('txt40', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=100)),
                ('placa', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=20)),
                ('chasis', models.CharField(max_length=50)),
                ('anho', models.CharField(max_length=20)),
                ('certificado', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Manifiesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=20)),
                ('fecha_emision', models.DateField(default=datetime.date.today)),
                ('documento', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='manifiesto.manifiestodoc')),
                ('vehiculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='manifiesto.vehiculo')),
            ],
        ),
    ]
