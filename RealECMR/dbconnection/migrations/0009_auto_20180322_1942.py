# Generated by Django 2.0.3 on 2018-03-23 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconnection', '0008_auto_20180322_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprador',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('buena', 'b'), ('normal', 'n'), ('mala', 'm')], default='b', max_length=6),
        ),
        migrations.AlterField(
            model_name='comprador',
            name='sexo',
            field=models.CharField(blank=True, choices=[('femenino', 'f'), ('masculino', 'm')], default='f', max_length=8),
        ),
        migrations.AlterField(
            model_name='intermediario',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('buena', 'b'), ('normal', 'n'), ('mala', 'm')], default='b', max_length=6),
        ),
        migrations.AlterField(
            model_name='intermediario',
            name='sexo',
            field=models.CharField(blank=True, choices=[('femenino', 'f'), ('masculino', 'm')], default='f', max_length=8),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('buena', 'b'), ('normal', 'n'), ('mala', 'm')], default='b', max_length=6),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='sexo',
            field=models.CharField(blank=True, choices=[('femenino', 'f'), ('masculino', 'm')], default='f', max_length=8),
        ),
    ]
