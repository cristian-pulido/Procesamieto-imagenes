# encoding: utf-8
import json
import os, shutil
from fileinput import filename

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

import string
import random

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
        