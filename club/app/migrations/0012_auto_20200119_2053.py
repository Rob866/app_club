# Generated by Django 2.2.6 on 2020-01-20 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20200119_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete_inscrito',
            name='horas_consumidas',
            field=models.CharField(default='00:00:00', max_length=100),
        ),
        migrations.AlterField(
            model_name='paquete_inscrito',
            name='horas_restantes',
            field=models.CharField(default='00:00:00', max_length=100),
        ),
    ]
