# Generated by Django 2.0.2 on 2018-03-22 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconnection', '0003_auto_20180320_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propiedad',
            name='tamano',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, null=True),
        ),
    ]