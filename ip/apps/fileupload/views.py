# encoding: utf-8
import json
import os, shutil
from fileinput import filename
from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import  redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView

from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize

from django.contrib.auth.models import Group, Permission, User

from apps.validacion.templatetags.scripts_validacion import proceso_inicial

from apps.validacion.forms import SeleccionForm
from apps.validacion.models import Imagenesdefecto, img_to_show

from apps.fileupload.models import Picture

import string
import random

import nibabel


class PictureCreateView(CreateView):
    model = Picture
    fields = ["file","slug"]


    def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        
        user_pk = str(self.object.slug)
        user = User.objects.get(pk=user_pk)
        group = user.groups.all()[0]

        self.object.user = user
        self.object.group = group

        self.object.save()

        self.object.slug=self.object.pk

        self.object.save()

        media=settings.MEDIA_ROOT
        
        folder_root=os.path.join(media,"root")
        
        if not os.path.exists(folder_root):
            os.mkdir(folder_root)

        folder_user=os.path.join(folder_root,"user_"+str(user.pk))

        if not os.path.exists(folder_user):
            os.mkdir(folder_user)

        folder_img= os.path.join(folder_user,"img_"+str(self.object.pk))            
        if os.path.exists(folder_img):
            shutil.rmtree(folder_img)
        os.mkdir(folder_img)

        shutil.move(self.object.file.path,folder_img)

        new_file=os.path.join(folder_img,os.path.basename(self.object.file.name))

        self.object.file=new_file[len(media):]

        self.object.save()

        proceso_inicial.delay(self.object.pk)

        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)

        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'fileupload.delete_picture'
    model = Picture
    template_name = 'fileupload/eliminar.html'
    # a donde va dirigido
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return redirect('login')


class PictureListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'fileupload.add_picture'
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

class PictureView(DetailView):
    model = Picture
    template_name = 'fileupload/informacion.html'    
    
class PictureViewImg(DetailView):
    model = Picture
    template_name = 'base/slice.html'
    
    
def Select(request,pk):
    form = SeleccionForm()
    object = Picture.objects.get(pk=pk)
    context={
      'object':object,
      'form': form,
    }
    
    
    
    if request.method == "POST":
        form = SeleccionForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            picture_pk=data['picture_pk']
            lista=data['lista_img']
            errores=[]
            img_s=lista.split(',')[:-1]
            
            temporal={}
            
            for i in img_s:
                img_pk,s_pk = i.split('_')
                temporal[int(img_pk)]=int(s_pk)
                img = img_to_show.objects.get(pk=img_pk)
                s = Imagenesdefecto.objects.get(pk=s_pk)
                
                file_path=settings.MEDIA_ROOT+img.path[len('/media'):]
                img_load=nibabel.load(file_path)
                
                if s.nombre == 'Estructural T1':
                    
                    
                    if len(img_load.shape) != 3:
                        errores.append("La imagen "+str(img)+" no puede ser Estructural T1 ya que no es 3-D")
                        
                if s.nombre == 'Funcional Resting':
                
                    if len(img_load.shape) <= 3:
                        errores.append("La imagen "+str(img)+" no puede ser Funcional Resting ya que tiene menos de 4 Dimensiones")
                        
                if s.nombre == 'DWI':
                    
                    if len(img_load.shape) <= 3:
                        errores.append("La imagen "+str(img)+" no puede ser del tipo DWI ya que tiene menos de 4 Dimensiones")
                        
                    if not os.path.exists(os.path.join(os.path.dirname(file_path),str(img)+".bvec" )):
                        errores.append("La imagen "+str(img)+" no puede del tipo DWI no se encontro el archivo bvec asociado")
                    if not os.path.exists(os.path.join(os.path.dirname(file_path),str(img)+".bval" )):
                        errores.append("La imagen "+str(img)+" no puede del tipo DWI no se encontro el archivo bval asociado")
                        
                    
                    
                    
                
            if len(errores) > 0:
                form = SeleccionForm()
                context['error']=errores
                return render(request, 'fileupload/seleccion.html',context)
            else:
                I=img_to_show.objects.filter(sujeto=str(picture_pk))
                
                
                for img in I:
                    
                    if img.pk in temporal:
                        s = Imagenesdefecto.objects.get(pk=temporal[img.pk])
                        img.img_defecto = s
                        img.save()
                    else:
                        img.img_defecto = None
                        img.save()
                        
                P=Picture.objects.get(pk=picture_pk)
                P.identificado = True
                P.save()
                        
               
                
                
                return redirect('picture',pk=picture_pk)
                
    
    if request.method == "GET":
        form = SeleccionForm()
    
    return render(request, 'fileupload/seleccion.html', context)
        
def edit_selection(request,picture_pk):
    
    picture = Picture.objects.get(pk=pk)  
    picture.identificado = False
    picture.save()
    
    return Select(request,picture_pk)
    
