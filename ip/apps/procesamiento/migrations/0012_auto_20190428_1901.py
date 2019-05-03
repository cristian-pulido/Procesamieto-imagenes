# Generated by Django 2.1.7 on 2019-04-29 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procesamiento', '0011_auto_20190427_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pipeline',
            name='tipo_imagen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='validacion.Imagenesdefecto'),
        ),
        migrations.AlterField(
            model_name='task',
            name='tipo_imagen',
            field=models.ForeignKey(on_delete=None, to='validacion.Imagenesdefecto'),
        ),
        migrations.AlterField(
            model_name='taskgroup',
            name='tipo_imagen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='validacion.Imagenesdefecto'),
        ),
    ]
