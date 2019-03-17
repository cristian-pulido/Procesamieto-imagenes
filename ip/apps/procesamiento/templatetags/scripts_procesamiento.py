from django import template
from programas.dcm2niix import T1_path,DWI_path,rest_path
from apps.validacion.models import Tipoimagenes
from django.conf import settings
from programas.definitions import results
import os
from apps.validacion.models import img_to_show
from apps.procesamiento.models import Task, Taskgroup, Pipeline, task_celery
import shutil
from programas.workflows import run_pipeline
from celery import shared_task

register = template.Library()

@register.simple_tag
def get_task_for_images(img):
    return img.task_set.all()

@register.simple_tag
def get_groups_for_images(img):
    return img.taskgroup_set.all()

@register.simple_tag
def get_img_with_tasks():
    T=Task.objects.all()
    imgs=[]
    for t in T:
        if t.tipo_imagen in imgs:
            continue
        else:
            imgs.append(t.tipo_imagen)
            
    return imgs

@register.simple_tag
def get_taskgroups():
    
    return Taskgroup.objects.all()

@register.simple_tag
def get_pipelines():
    
    return Pipeline.objects.all()

@register.simple_tag
def get_estado_pipeline(pipeline,img):
        
    return task_celery.objects.filter(imagen=img,pipeline=pipeline)


@register.simple_tag
def tareas_defecto():
    
    DWI=Tipoimagenes.objects.get_or_create(nombre="TENSOR  AXI")[0]
    
    P=Pipeline.objects.filter(nombre="Pipeline Difusion",tipo_imagen=DWI)
    folder_tareas=os.path.join(settings.BASE_DIR,"tareas")
    
    if len(P) == 0 :
                
        eddy=Task.objects.get_or_create(nombre="eddy correction",
                                        pathscript=os.path.join(folder_tareas,"eddy_correction.py"),
                                        tipo_imagen=DWI)[0]
        nlm=Task.objects.get_or_create(nombre="Non Local Mean",
                                       pathscript=os.path.join(folder_tareas,"nonLocalMean.py"),
                                       tipo_imagen=DWI)[0]
        reslicing=Task.objects.get_or_create(nombre="Reslicing",
                                             pathscript=os.path.join(folder_tareas,"reslicing.py"),
                                             tipo_imagen=DWI)[0]
        bet_dwi=Task.objects.get_or_create(nombre="Bet DWI",
                                           pathscript=os.path.join(folder_tareas,"betDWI.py"),
                                           tipo_imagen=DWI)[0]
        dwi_2_mni=Task.objects.get_or_create(nombre="To register dwi to MNI",
                                             pathscript=os.path.join(folder_tareas,"to_register_dwi_to_mni.py"),
                                             tipo_imagen=DWI,
                                             dependencia=bet_dwi)[0]
        estimate_dti=Task.objects.get_or_create(nombre="To estimate dti",
                                                pathscript=os.path.join(folder_tareas,"to_estimate_dti.py"),
                                                tipo_imagen=DWI,
                                                dependencia=bet_dwi)[0]
        estimate_dti_maps=Task.objects.get_or_create(nombre="To estimate dti maps",
                                                     pathscript=os.path.join(folder_tareas,"to_estimate_dti_maps.py"),
                                                     tipo_imagen=DWI,
                                                     dependencia=estimate_dti)[0]
        generate_bundles=Task.objects.get_or_create(nombre="To Generate Bunddle",
                                                    pathscript=os.path.join(folder_tareas,"to_generate_bunddle.py"),
                                                    tipo_imagen=DWI,
                                                    dependencia=dwi_2_mni)[0]
        generate_tracto=Task.objects.get_or_create(nombre="To Generate Tractography",
                                                   pathscript=os.path.join(folder_tareas,"to_generate_tractography.py"),
                                                   tipo_imagen=DWI,
                                                   dependencia=bet_dwi)[0]
        pre_DWI=Taskgroup.objects.get_or_create(nombre="Preprocesamiento DWI",tipo_imagen=DWI,eliminable=False)[0]
        task_pre_dwi=[eddy,nlm,reslicing,bet_dwi,dwi_2_mni]
        orden=""
        for t in task_pre_dwi:
            pre_DWI.task.add(t)
            orden+=str(t.pk)+"_"
        pre_DWI.orden=orden
        pre_DWI.save()
        
        post_DWI=Taskgroup.objects.get_or_create(nombre="Postprocesamiento DWI",tipo_imagen=DWI,dependencia=pre_DWI,
                                                 eliminable=False)[0]
        task_post_dwi=[estimate_dti,estimate_dti_maps,generate_bundles,generate_tracto]
        orden=""
        for t in task_post_dwi:
            post_DWI.task.add(t)
            orden+=str(t.pk)+"_"
        post_DWI.orden=orden
        post_DWI.save()
        
        P_DWI=Pipeline.objects.get_or_create(nombre="Pipeline Difusion",
                                             tipo_imagen=DWI,eliminable=False)[0]
        groups_P=[pre_DWI,post_DWI]
        orden=""
        for t in groups_P:
            P_DWI.grupos.add(t)
            orden+=str(t.pk)+"_"
        P_DWI.orden=orden
        P_DWI.save()
        
    return ""


def validar_orden(tareas):
    flag = True
    for t in range(len(tareas)):
        if tareas[t].dependencia:
            if tareas[t].dependencia not in tareas[:t]:
                flag=False
                
    return flag

def get_task_list(pipeline):
    tareas=[]
    for g in pipeline.get_groups():
        for t in g.get_tasks():
            if t not in tareas:
                tareas.append(t)
            
    return tareas

def organizar(tareas):
    while(validar_orden(tareas) == False):
        for t in tareas:
            if t.dependencia:
                if t.dependencia in tareas[tareas.index(t):]:
                    tareas.remove(t.dependencia)
                    break
                elif t.dependencia not in tareas:
                    tareas.insert(tareas.index(t),t.dependencia)
                    break
                else:
                    continue


@shared_task
def crear_tarea(pk):
    
    t_celery = task_celery.objects.get(pk=pk)
    
    if not os.path.exists(results):
        os.mkdir(results)
        
    folder_user= os.path.join(results,"user_"+str(t_celery.user.pk))
    
    if not os.path.exists(folder_user):
        os.mkdir(folder_user)
        
    folder_img= os.path.join(folder_user,"img_"+str(t_celery.imagen.pk))
    
    if not os.path.exists(folder_img):
        os.mkdir(folder_img)
        
    folder_pipeline = os.path.join(folder_img,str(t_celery.pipeline.pk))
    
    if not os.path.exists(folder_pipeline):
        os.mkdir(folder_pipeline)
        
    tareas=get_task_list(t_celery.pipeline)
    organizar(tareas)
    
    media=settings.MEDIA_ROOT
    
    folder_nii=os.path.join(os.path.dirname(media+t_celery.imagen.file.name),"nifty")
    
    archives=[T1_path(folder_nii)]+DWI_path(folder_nii)+[rest_path(folder_nii)]
    
    for file in archives:
        shutil.copy(file,folder_pipeline)
        
    img=img_to_show.objects.get(sujeto=t_celery.imagen,imagen=t_celery.pipeline.tipo_imagen)
    
    path_in=os.path.join(folder_pipeline,os.path.basename(img.path))
    
    dic_tareas={}
    for i in range(len(tareas)):
            dic_tareas[i]=[str(tareas[i].pk),tareas[i].pathscript,[path_in]]
    path_in=run_pipeline("g",dic_tareas,folder_pipeline)
    
    if path_in != "error":
        t_celery.estado="Finalizado"
        t_celery.save()
    else:
        t_celery.estado="Finalizado con Error"
        t_celery.save()
    

    
    return ""
        