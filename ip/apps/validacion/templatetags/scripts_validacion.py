from apps.validacion.models import Tipoimagenes, Tagsdicom, Campostagimg, Campos_defecto, Parametrosmotioncorrect, img_to_show
from apps.fileupload.models import Picture
from django import template
from django.conf import settings
import os, shutil
from celery import shared_task

from programas.anonimizador import dicom_anonymizer, get_tags_dicom
from django.contrib.auth.models import Group, Permission, User

from programas.dcm2niix import convertir_dcm_2_nii, T1_path, DWI_path, rest_path
from programas.motion_correct_fmri import func_motion_correct

from apps.procesamiento.models import Taskgroup, Task

register = template.Library()

def pass_tags_to_db(pk,series):
    for serie in series:
        TipoImg=Tipoimagenes.objects.get_or_create(nombre=serie)[0]
        for tag in series[serie]:
            num_tag=series[serie][tag]["num_tag"]
            name_tag=tag
            key_tag=series[serie][tag]["name_tag"]
            Tag=Tagsdicom.objects.get_or_create(num_tag=num_tag,name_tag=name_tag,key_tag=key_tag)[0]
            picture=Picture.objects.get(pk=pk)
            CampoTag=Campostagimg.objects.create(tag=Tag,
                                                valor=series[serie][tag]["v_tag"],
                                                imagen=TipoImg,
                                                user=picture.user,
                                                img_user=picture
                                               )

@register.simple_tag
def get_filters_by_user(user_pk):
    user=User.objects.get(pk=user_pk)
    C=Campos_defecto.objects.filter(user=user)
    return C




def campos_a_mostrar(user_pk):
    user=User.objects.get(pk=user_pk)
    default=Campos_defecto.objects.filter(user=user)
    for d in default:
        campo=Campostagimg.objects.filter(tag=d.tag,imagen=d.imagen,user=user)
        for c in campo:
            c.medidas=d.medidas
            c.save()
            c.precision=d.precision
            c.save()
            c.v_esperado=d.v_esperado
            c.save()

            if c.precision == "" or c.precision == None:
                c.precision = 0
                c.save()

            if c.v_esperado == "" or c.v_esperado == None:
                continue
            else:
                sup=float(c.v_esperado)*(1+float(c.precision)/100)
                inf = float(c.v_esperado) * (1 - float(c.precision) / 100)
                if float(c.v_esperado) >= inf and float(c.v_esperado) <= sup:
                    c.cumple = True
                else:
                    c.cumple = False
                c.save()

    return ""

@register.simple_tag
def get_name_images(campos_defecto):
    I=[]
    for c in campos_defecto:
        if c.imagen in I:
            continue
        else:
            I.append(c.imagen)
    return I

@register.simple_tag
def get_tags_images(nombre,user_pk):
    I = Tipoimagenes.objects.get(nombre=nombre)
    C = Campos_defecto.objects.filter(imagen=I,user=user_pk)
    return C

@register.simple_tag
def get_name_images_by_file(file_pk):
    picture=Picture.objects.get(pk=file_pk)
    campos_img=Campostagimg.objects.filter(img_user=picture)

    images=[]

    for img in campos_img:
        if img.imagen in images:
            continue
        else:
            if len(get_tags_images(img.imagen,picture.user.pk)) > 0:
                images.insert(0,img.imagen)
            else:
                images.append(img.imagen)
    return images





@register.simple_tag
def get_camp_images_by_tag(nombre_tag,file):

    C = Campostagimg.objects.get(tag=nombre_tag.tag,imagen=nombre_tag.imagen,user=nombre_tag.user,img_user=file)
    return C



@shared_task
def proceso_inicial(picture_pk):

	media=settings.MEDIA_ROOT

	picture=Picture.objects.get(pk=picture_pk)

	file_path=media+picture.file.name

	base_dir = os.path.dirname(file_path)

	folder_dicom = os.path.join(base_dir, "imagenes")

	os.mkdir(folder_dicom)


	shutil.move(file_path, folder_dicom)

	archive=os.path.join(folder_dicom,os.listdir(folder_dicom)[0])
	import zipfile
	a=zipfile.ZipFile(archive)
	a.extractall(folder_dicom)

	dicom_anonymizer(folder_dicom)

	picture.anonimo = True

	picture.save()

	series=get_tags_dicom(folder_dicom)
	pass_tags_to_db(picture_pk,series)
	campos_a_mostrar(picture.user.pk)

	folder_nii = os.path.join(base_dir, "nifty")
	os.mkdir(folder_nii)
	convertir_dcm_2_nii(base_dir, folder_nii)

	zip_name = os.path.join(base_dir, "img_"+str(picture_pk)+"_dicom")
	carpeta = folder_dicom
	shutil.make_archive(zip_name, 'zip', carpeta)
	shutil.rmtree(folder_dicom)


	carpeta = folder_nii
	shutil.make_archive(os.path.splitext(file_path)[0], 'zip', carpeta)

	files = [[T1_path(folder_nii)], DWI_path(folder_nii), [rest_path(folder_nii)]]
	folder_filter=os.path.join(base_dir,"filter")
	os.mkdir(folder_filter)

	for i in files:
		for j in i:
			shutil.copy(j,folder_filter)
	shutil.rmtree(folder_nii)
	os.rename(folder_filter,folder_nii)

	structural_result=os.path.join(folder_nii, "structural_result")
	os.mkdir(structural_result)

	archive=T1_path(folder_nii)
	img_to_show.objects.create(sujeto=picture,
                               imagen=Tipoimagenes.objects.get_or_create(nombre='3D AX Obl T1 FSPGR')[0],
                               path=archive[len(settings.MEDIA_ROOT[:-6]):])

	func_result=os.path.join(folder_nii, "func_result")
	absolute_func, relative_func , paths_html_func= func_motion_correct(rest_path(folder_nii), func_result,picture.get_name(),"func")
	os.remove(rest_path(folder_nii))
	shutil.move(rest_path(func_result), folder_nii)

	archive=rest_path(folder_nii)

	img_to_show.objects.create(sujeto=picture,
                               imagen=Tipoimagenes.objects.get_or_create(nombre='RESTING')[0],
                               path=archive[len(settings.MEDIA_ROOT[:-6]):])

	P = Parametrosmotioncorrect.objects.create(imagen=picture,
                                               absolute_func=absolute_func,
                                               relative_func=relative_func,
                                               graphic_desplazamiento_func=paths_html_func["desplazamiento"],
                                               graphic_rotacion_func=paths_html_func["rotaciones"],
                                               graphic_traslacion_func= paths_html_func["traslaciones"])
	P.save()
    
	archive=DWI_path(folder_nii,False)
       
	img_to_show.objects.create(sujeto=picture,
                               imagen=Tipoimagenes.objects.get_or_create(nombre='TENSOR  AXI')[0],
                               path=archive[len(settings.MEDIA_ROOT[:-6]):])
    
	return "completo"



