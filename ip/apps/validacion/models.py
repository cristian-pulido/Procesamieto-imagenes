from django.db import models

from django.contrib.auth.models import Group, Permission, User

from apps.fileupload.models import Picture
from django.conf import settings
import os
# Create your models here.


class Tipoimagenes(models.Model):
    nombre = models.CharField(max_length=75)
    nombre_aux = models.CharField(max_length=75,null=True,blank=True,default="")
    mostrar = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.nombre)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields
        
        
class Imagenesdefecto(models.Model):
    nombre = models.CharField(max_length=75)

    def __str__(self):
        return '{}'.format(self.nombre)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


class Tagsdicom(models.Model):
    num_tag = models.CharField(max_length=75)
    name_tag = models.CharField(max_length=200)
    key_tag = models.CharField(max_length=200,blank=True,null=True  )

    def __str__(self):
        return '{}'.format(self.name_tag)
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields


class Campostagimg(models.Model):
    tag = models.ForeignKey(Tagsdicom, on_delete=models.CASCADE)
    valor = models.CharField(max_length=200,null=True,blank=True,default="")
    medidas = models.CharField(max_length=50,null=True,blank=True,default="")
    imagen = models.ForeignKey(Tipoimagenes,on_delete=models.CASCADE)

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)    
    img_user = models.ForeignKey(Picture,on_delete=models.CASCADE,null=True) 
    precision = models.PositiveIntegerField(null=True,blank=True)
    v_esperado = models.CharField(max_length=150,null=True,blank=True,default="")
    cumple = models.NullBooleanField(default=None)

    def __str__(self):
        return 'User %s - imagen %s' % (self.user,self.imagen)
    class Meta:
        permissions = (
            ("can_ver_parametrosimg", u"puede ver parametrosimg"),


        )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields

class Campos_defecto(models.Model):
    imagen = models.ForeignKey(Tipoimagenes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tagsdicom, on_delete=models.CASCADE)
    precision = models.PositiveIntegerField(null=True, blank=True)
    v_esperado = models.CharField(max_length=150, null=True, blank=True, default="")
    medidas = models.CharField(max_length=50, null=True, blank=True, default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return '{}'.format(self.tag.name_tag)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        campo = Campostagimg.objects.filter(tag=self.tag, imagen=self.imagen)
        for c in campo:
            c.medidas = ""
            c.save()
            c.precision = 0
            c.save()
            c.v_esperado = ""
            c.save()       

        super(Campos_defecto, self).delete(*args, **kwargs)

    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields



    
class Parametrosmotioncorrect(models.Model):
    imagen = models.OneToOneField(Picture, on_delete=models.CASCADE, null=True, blank=True)
    
    absolute_func = models.CharField(max_length=50, null=True)
    relative_func = models.CharField(max_length=50, null=True)
    graphic_desplazamiento_func = models.CharField(max_length=300,null=True,blank=True)
    graphic_rotacion_func= models.CharField(max_length=300,null=True,blank=True)
    graphic_traslacion_func= models.CharField(max_length=300,null=True,blank=True)
    aceptado_func = models.NullBooleanField()

    class ReportBuilder:
        exclude = ('id',)  # Lists or tuple of excluded fields
        
class img_to_show(models.Model):
    sujeto = models.ForeignKey(Picture,on_delete=models.CASCADE)
    imagen = models.ForeignKey(Tipoimagenes,on_delete=models.CASCADE)
    path = models.CharField(max_length=300, null=True, blank=True)
    img_defecto = models.ForeignKey(Imagenesdefecto,on_delete=models.CASCADE,null=True,blank=True)
    


    
    
    
    
    def __str__(self):
        path=self.path
        if ".nii.gz" in path:

            return '{}'.format(os.path.basename(path)[:-len(".nii.gz")])
        elif ".nii" in path:

            return '{}'.format(os.path.basename(path)[:-len(".nii")])
        else:
            return '{}'.format(os.path.basename(path))
    class Meta:
        ordering = ['path']
        permissions = (
            ("can_ver_slice", u"puede ver slice"),

            )
    class ReportBuilder:
        exclude = ('id', )  # Lists or tuple of excluded fields
        
    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""

        user_n=str(self.sujeto.user.pk)
        img_name=str(self.sujeto.pk)
        
        file_path=settings.MEDIA_ROOT+self.path[len('/media'):]

        os.remove(file_path)
        super(img_to_show, self).delete(*args, **kwargs)