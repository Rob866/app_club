# Generated by Django 2.2.9 on 2020-02-03 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0020_auto_20200201_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=60, unique=True),
        ),
    ]
