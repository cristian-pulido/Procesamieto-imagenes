from django import template
import os
import shutil
from django.contrib.auth.models import Group, Permission, User
from django.conf import settings
from apps.fileupload.models import Picture
from apps.validacion.models import Imagenesdefecto

register = template.Library()


@register.simple_tag
def creargrupos():
    # permisos

    # imagenes
    p1 = Permission.objects.get(name="Can add picture")
    p2 = Permission.objects.get(name="Can change picture")
    p3 = Permission.objects.get(name="Can delete picture")
    
    p4 = Permission.objects.get(name="puede ver slice")

    
    ## creacion grupos
    prueba = Group.objects.get_or_create(name='Prueba')[0]
    
    prueba.permissions.add(p1,p2,p3,p4)
    

    users = User.objects.all()
    for i in users:
        if len(i.groups.all()) == 0:
            prueba.user_set.add(i)


    return ""

@register.simple_tag
def crearimgdefecto():
    

    # imagenes
    t1 = Imagenesdefecto.objects.get_or_create(nombre="Estructural T1")
    resting = Imagenesdefecto.objects.get_or_create(nombre="Funcional Resting")
    dwi = Imagenesdefecto.objects.get_or_create(nombre="DWI")
    
    
    return ""

@register.simple_tag
def mostrarimgdefecto():     
    
    return Imagenesdefecto.objects.all()


@register.simple_tag
def get_archivos(pk):
    
    user=User.objects.get(pk=pk)
    P=Picture.objects.filter(user=user)
    return P

@register.simple_tag
def get_archivos_group(pk):
    
    user=User.objects.get(pk=pk)
    group=user.groups.all()[0]
    result=[]
    for u in group.user_set.all():
        if u != user:
            result+=get_archivos(u.pk)
    return result

@register.simple_tag
def create_user_test():
    try: 
        User.objects.create_user(username='user',password='pass',first_name='user_test') 
    except: 
        pass
    return ""