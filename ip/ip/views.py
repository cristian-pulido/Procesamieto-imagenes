
from django.shortcuts import render, redirect

from django.contrib.auth.models import Group, Permission, User
from apps.fileupload.models import Picture
from apps.procesamiento.models import Task, Taskgroup, Pipeline, task_celery, config
from apps.procesamiento.templatetags.scripts_procesamiento import crear_tarea


def reportes(request):
    return render(request,'base/reportes.html')

def lista(request):
    return render(request,'base/lista.html')


def carga(request):
    return render(request,'base/carga.html')


def run_pipeline(request,user_pk,config_pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user=User.objects.get(pk=user_pk)
        conf=config.objects.get(pk=config_pk)
        
        
        t_celery=task_celery.objects.create(user=user,configuracion=conf,
                                            estado="Ejecutando")
        
        tarea=crear_tarea.delay(t_celery.pk)
        
        t_celery.id_task=tarea.task_id
        t_celery.save()
        
        return redirect("login")
        
    
    