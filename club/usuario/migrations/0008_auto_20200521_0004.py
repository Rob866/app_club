# Generated by Django 2.2.9 on 2020-05-21 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_auto_20200520_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='grupo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
    ]
