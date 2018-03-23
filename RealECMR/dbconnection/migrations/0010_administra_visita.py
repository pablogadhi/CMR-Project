# Generated by Django 2.0.3 on 2018-03-23 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbconnection', '0009_auto_20180322_1942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(null=True)),
                ('intermediario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dbconnection.Intermediario')),
                ('propiedad', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dbconnection.Propiedad')),
                ('propietario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dbconnection.Propietario')),
            ],
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(null=True)),
                ('comprador', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dbconnection.Comprador')),
                ('intermediario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dbconnection.Intermediario')),
                ('propiedad', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dbconnection.Propiedad')),
            ],
        ),
    ]
