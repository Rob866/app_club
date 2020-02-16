# Generated by Django 2.2.9 on 2020-02-16 05:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Historial_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Actividad de los Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('mensaje', models.TextField()),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Envio de Notificaciones a grupos',
            },
        ),
        migrations.CreateModel(
            name='Paquete_Inscrito',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='id del Paquete', primary_key=True, serialize=False)),
                ('fecha_de_inscripcion', models.DateField(blank=True, null=True)),
                ('horas_consumidas', models.CharField(default='00:00:00 Hrs', max_length=100)),
                ('horas_restantes', models.CharField(default='00:00:00 Hrs', max_length=100)),
                ('tiempo_consumido', models.DurationField(default=datetime.timedelta(0))),
                ('tiempo_restante', models.DurationField(default=datetime.timedelta(0))),
                ('status', models.BooleanField(blank=True, choices=[(True, 'Activo'), (False, 'Finalizado')], default=True, help_text='Elige el estado del paquete')),
            ],
            options={
                'verbose_name': 'Paquete Inscrito',
                'verbose_name_plural': 'Paquetes Inscritos',
                'ordering': ['usuario__nombre'],
            },
        ),
        migrations.CreateModel(
            name='Tipo_de_Paquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Tipo de Paquete',
                'verbose_name_plural': 'Tipos de Paquetes',
            },
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignatura', models.CharField(max_length=100)),
                ('tiempo_de_inicio', models.DateTimeField(blank=True, null=True)),
                ('tiempo_de_salida', models.DateTimeField(blank=True, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=200, null=True)),
                ('paquete_inscrito', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sesiones', to='app.Paquete_Inscrito')),
            ],
            options={
                'verbose_name': 'Sesion',
                'verbose_name_plural': 'Sesiones',
                'ordering': ['-tiempo_de_inicio'],
            },
        ),
        migrations.AddField(
            model_name='paquete_inscrito',
            name='tipo_de_paquete',
            field=models.ForeignKey(help_text='Elige el tipo de paquete del alumno', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Tipo_de_Paquete'),
        ),
    ]
