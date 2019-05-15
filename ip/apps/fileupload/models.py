# encoding: utf-8
import os
import shutil

from django.db import models
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.models import Group, Permission, User
from django.conf import settings



class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.FileField(upload_to="Archivos")
    slug = models.SlugField(max_length=100, blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    group = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True)
    anonimo = models.BooleanField(default=False)
    no_dicom = models.BooleanField(default=False)
    identificado = models.BooleanField(default=False)


    def __str__(self):
        #return self.file.name
        return '{}'.format(self.slug)



    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)


    def get_name(self):

        return os.path.splitext(os.path.basename(self.file.name))[0]



    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""

        user_n=str(self.user.pk)
        img_name=str(self.pk)

        folder=os.path.join(settings.MEDIA_ROOT,"root/user_"+user_n+"/img_"+img_name)
        shutil.rmtree(folder, ignore_errors=True)
        
        folder=os.path.join(settings.MEDIA_ROOT,"results/user_"+user_n+"/img_"+img_name)
        shutil.rmtree(folder, ignore_errors=True)

        super(Picture, self).delete(*args, **kwargs)



