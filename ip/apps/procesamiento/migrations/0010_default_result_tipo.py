# Generated by Django 2.1.7 on 2019-04-05 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procesamiento', '0009_default_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='default_result',
            name='tipo',
            field=models.CharField(choices=[('Imagen', 'Imagen'), ('Grafica', 'Grafica'), ('Texto', 'Texto'), ('Archivo nii', 'Archivo nii')], max_length=40, null=True),
        ),
    ]
