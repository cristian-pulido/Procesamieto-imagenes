from django.db import models

from apps.validacion.models import Tipoimagenes
from django.contrib.auth.models import Group, Permission, User
from apps.fileupload.models import Picture
# Create your models here.


class Task(models.Model):
    nombre = models.CharField(max_length=100)
    pathscript = models.CharField(max_length=150)
    dependencia = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    habilitado = models.BooleanField(default=True)
    tipo_imagen = models.ForeignKey(Tipoimagenes, on_delete=None)

    def __str__(self):
        return '{}'.format(self.nombre)


class Taskgroup(models.Model):

    nombre=models.CharField(max_length=100)
    task=models.ManyToManyField(Task, blank=True)
    orden=models.CharField(max_length=200,null=True)
    tipo_imagen = models.ForeignKey(Tipoimagenes, on_delete=models.CASCADE)
    dependencia = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,default=None,blank=True)
    eliminable = models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)

    def get_tasks(self):
        orden=self.orden
        lista=orden.split("_")[:-1]
        tareas = []
        
        for i in lista:
            tareas.append(Task.objects.get(pk=int(i)))
            
        return tareas
        
class Pipeline(models.Model):

    nombre=models.CharField(max_length=100)
    grupos=models.ManyToManyField(Taskgroup, blank=True)
    orden=models.CharField(max_length=200,null=True)
    tipo_imagen = models.ForeignKey(Tipoimagenes, on_delete=models.CASCADE)
    dependencia = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,default=None,blank=True)
    eliminable = models.BooleanField(default=True)
    def __str__(self):
        return '{}'.format(self.nombre)

    def get_groups(self):
        orden=self.orden
        lista=orden.split("_")[:-1]
        groups = []
        
        for i in lista:
            groups.append(Taskgroup.objects.get(pk=int(i)))
            
        return groups
        
        
class task_celery(models.Model):

    id_task=models.CharField(max_length=200,default="",blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    imagen = models.ForeignKey(Picture,on_delete=models.CASCADE,null=True)
    pipeline = models.ForeignKey(Pipeline,on_delete=models.CASCADE,null=True)
    estado = models.CharField(max_length=100)
    
    
    def __str__(self):
        return 'imagen %s - proceso %s' % (self.imagen.pk,self.pipeline.nombre)

        
        








