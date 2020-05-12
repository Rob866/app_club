# Generated by Django 2.2.9 on 2020-05-12 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('imagen', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('email', models.EmailField(blank=True, max_length=60)),
                ('facebook', models.CharField(blank=True, max_length=100)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('edad', models.IntegerField(blank=True, null=True)),
                ('padecimientos', models.TextField(blank=True, verbose_name='padecimientos')),
                ('asistencia', models.CharField(blank=True, max_length=100, verbose_name='Días de asistencia')),
                ('enfoque', models.CharField(blank=True, max_length=100, verbose_name='Area en la que guste que se enfocará la atención')),
                ('nombre_de_la_madre', models.CharField(blank=True, max_length=100, verbose_name='Nombre de la Madre')),
                ('edad_de_la_madre', models.IntegerField(blank=True, null=True, verbose_name='Edad')),
                ('ocupacion_de_la_madre', models.CharField(blank=True, max_length=100, verbose_name='Ocupación')),
                ('numero_de_la_madre', models.IntegerField(blank=True, null=True, verbose_name='Número de contacto')),
                ('nombre_del_padre', models.CharField(blank=True, max_length=100, verbose_name='Nombre del Padre')),
                ('edad_del_padre', models.IntegerField(blank=True, null=True, verbose_name='Edad')),
                ('ocupacion_del_padre', models.CharField(blank=True, max_length=100, verbose_name='Ocupación')),
                ('numero_del_padre', models.IntegerField(blank=True, null=True, verbose_name='Número de contacto')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('escuela', models.CharField(blank=True, max_length=100, verbose_name='Nombre de la escuela')),
                ('domicilio', models.CharField(blank=True, max_length=150, verbose_name='Domicilio')),
                ('status_paquetes', models.BooleanField(default=False, verbose_name='¿Tiene Paquetes Activos?')),
                ('nivel_academico', models.CharField(blank=True, max_length=500, verbose_name='Nivel académico del alumno')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de ingreso')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Ultima fecha de Sesión')),
                ('is_admin', models.BooleanField(default=False, verbose_name='¿Es Administrador?')),
                ('is_active', models.BooleanField(default=True, verbose_name='¿Esta Acivo?')),
                ('is_staff', models.BooleanField(default=False, verbose_name='¿Es parte del Staff?')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='¿Es Super Usuario?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
