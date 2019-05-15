from django.db import models

from apps.validacion.models import Tipoimagenes, Imagenesdefecto, img_to_show
from django.contrib.auth.models import Group, Permission, User
from apps.fileupload.models import Picture
# Create your models here.


class Task(models.Model):
    nombre = models.CharField(max_length=100)
    pathscript = models.CharField(max_length=150)
    dependencia = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    habilitado = models.BooleanField(default=True)
    tipo_imagen = models.ForeignKey(Imagenesdefecto, on_delete=None)

    def __str__(self):
        return '{}'.format(self.nombre)
    
class default_result(models.Model):

    nombre=models.CharField(max_length=100)
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    word_key=models.CharField(max_length=100)
    
    imagen='Imagen'
    grafica='Grafica'
    text="Texto"
    nii="Archivo nii"
    trk="Archivo trk"
    csv="Archivo csv"
    ica="Ica Component"
    g_ica="Ica Graph"
    
    tipo_choices=((imagen, u'Imagen'),(grafica, u'Grafica'),(text, u'Texto'),(nii, u'Archivo nii'),(trk, u'Archivo trk'),(csv, u'Archivo csv'),(ica, u'Ica Component'),(g_ica, u'Ica Graph'))
    tipo=models.CharField(max_length=40, choices=tipo_choices, null=True)    
    def __str__(self):
        return '{}'.format(self.nombre)


class Taskgroup(models.Model):

    nombre=models.CharField(max_length=100)
    task=models.ManyToManyField(Task, blank=True)
    orden=models.CharField(max_length=200,null=True)
    tipo_imagen = models.ForeignKey(Imagenesdefecto, on_delete=models.CASCADE)
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
    tipo_imagen = models.ForeignKey(Imagenesdefecto, on_delete=models.CASCADE)
    
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
    
class config(models.Model):

    entradas = models.ManyToManyField(img_to_show)
    pipeline = models.ForeignKey(Pipeline,on_delete=models.CASCADE,null=True)
    imagen = models.ForeignKey(Picture,on_delete=models.CASCADE,null=True)
    
    
    def __str__(self):
        return 'imagen %s - proceso %s' % (self.imagen.pk,self.pipeline.nombre)
        
        
class task_celery(models.Model):

    id_task=models.CharField(max_length=200,default="",blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    configuracion = models.ForeignKey(config,on_delete=models.CASCADE,null=True)
    estado = models.CharField(max_length=100)
    
    
    def __str__(self):
        return 'imagen %s - proceso %s' % (self.configuracion.imagen.pk,self.configuracion.pipeline.nombre)
    
    
class results(models.Model):

    task_celery = models.ForeignKey(task_celery,on_delete=models.CASCADE,null=True)
    nombre=models.CharField(max_length=100)
    path = models.CharField(max_length=250)
    
    imagen='Imagen'
    grafica='Grafica'
    text="Texto"
    nii="Archivo nii"
    trk="Archivo trk"
    csv="Archivo csv"
    ica="Ica Component"
    g_ica="Ica Graph"
    
    tipo_choices=((imagen, u'Imagen'),(grafica, u'Grafica'),(text, u'Texto'),(nii, u'Archivo nii'),(trk, u'Archivo trk'),(csv, u'Archivo csv'),(ica, u'Ica Component'),(g_ica, u'Ica Graph'))
    tipo=models.CharField(max_length=40, choices=tipo_choices, null=True)
    
    def __str__(self):
        return 'imagen:  %s - nombre: %s' % (self.task_celery.configuracion.imagen.get_name(),self.nombre)

        
        








