# Generated by Django 2.2.9 on 2020-05-21 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200513_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
    ]
