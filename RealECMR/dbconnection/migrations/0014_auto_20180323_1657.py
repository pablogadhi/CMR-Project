# Generated by Django 2.0.3 on 2018-03-23 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconnection', '0013_auto_20180323_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprador',
            name='tipoPropiedad',
            field=models.CharField(blank=True, choices=[('Apartamento', 'Apartamento'), ('Casa', 'Casa'), ('Terreno', 'Terreno'), ('Otro', 'Otro')], max_length=10),
        ),
    ]