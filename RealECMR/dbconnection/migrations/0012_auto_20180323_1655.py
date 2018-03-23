# Generated by Django 2.0.3 on 2018-03-23 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconnection', '0011_auto_20180323_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprador',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('Buena', 'buena'), ('Normal', 'normal'), ('Mala', 'buena')], max_length=10),
        ),
        migrations.AlterField(
            model_name='comprador',
            name='sexo',
            field=models.CharField(blank=True, choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino')], max_length=10),
        ),
        migrations.AlterField(
            model_name='intermediario',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('Buena', 'buena'), ('Normal', 'normal'), ('Mala', 'buena')], max_length=10),
        ),
        migrations.AlterField(
            model_name='intermediario',
            name='sexo',
            field=models.CharField(blank=True, choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino')], max_length=10),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='tipo',
            field=models.CharField(blank=True, choices=[('Apartamento', 'apartamento'), ('Casa', 'casa'), ('Terreno', 'terreno'), ('Otro', 'otro')], max_length=10),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='reputacion',
            field=models.CharField(blank=True, choices=[('Buena', 'buena'), ('Normal', 'normal'), ('Mala', 'buena')], max_length=10),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='sexo',
            field=models.CharField(blank=True, choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino')], max_length=10),
        ),
    ]