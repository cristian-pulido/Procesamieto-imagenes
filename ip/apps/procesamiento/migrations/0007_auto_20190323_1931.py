# Generated by Django 2.1.7 on 2019-03-24 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procesamiento', '0006_task_celery'),
    ]

    operations = [
        migrations.CreateModel(
            name='results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='task_celery',
            name='id_task',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='results',
            name='task_celery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procesamiento.task_celery'),
        ),
    ]
