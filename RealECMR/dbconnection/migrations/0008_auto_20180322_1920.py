# Generated by Django 2.0.3 on 2018-03-23 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconnection', '0007_auto_20180322_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comprador',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='intermediario',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='propietario',
            name='rol',
        ),
        migrations.AddField(
            model_name='comprador',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('b', 'buena'), ('n', 'normal'), ('m', 'mala')], default='b', max_length=1),
        ),
        migrations.AddField(
            model_name='intermediario',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('b', 'buena'), ('n', 'normal'), ('m', 'mala')], default='b', max_length=1),
        ),
        migrations.AddField(
            model_name='propietario',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('b', 'buena'), ('n', 'normal'), ('m', 'mala')], default='b', max_length=1),
        ),
        migrations.AlterField(
            model_name='comprador',
            name='sexo',
            field=models.CharField(blank=True, choices=[('f', 'femenino'), ('m', 'masculino')], default='f', max_length=1),
        ),
        migrations.AlterField(
            model_name='intermediario',
            name='sexo',
            field=models.CharField(blank=True, choices=[('f', 'femenino'), ('m', 'masculino')], default='f', max_length=1),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='sexo',
            field=models.CharField(blank=True, choices=[('f', 'femenino'), ('m', 'masculino')], default='f', max_length=1),
        ),
    ]
