# Generated by Django 2.2.6 on 2020-01-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0015_auto_20200130_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(help_text='Si no cuentas con un email deja este valor por dafault', max_length=60, unique=True),
        ),
    ]