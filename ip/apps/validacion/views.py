from django.shortcuts import render, redirect

# Create your views here.

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from apps.validacion.forms import Campos_defectoForm
from apps.validacion.models import Campos_defecto, Campostagimg, img_to_show
from apps.validacion.templatetags.scripts_validacion import campos_a_mostrar


class Campos_defectoCreate(CreateView):
    model = Campos_defecto
    form_class = Campos_defectoForm
    template_name = 'validacion/filtro_form.html'


    def get_success_url(self):
        o = self.object
        if o.precision == None:
            o.precision = 0
        if o.v_esperado == None:
            o.v_esperado = ""
        if o.medidas == None:
            o.medidas = ""
        o.save()
        campos_a_mostrar(self.object.user.pk)
        return reverse_lazy('filtro_listar')
       
class Campos_defectoUpdate(UpdateView):
    model = Campos_defecto
    form_class = Campos_defectoForm
    template_name = 'validacion/filtro_form.html'
    # a donde va dirigido
    def get_success_url(self):
        o = self.object
        if o.precision == None:
            o.precision = 0
        if o.v_esperado == None:
            o.v_esperado = ""
        if o.medidas == None:
            o.medidas = ""
        o.save()
        campos_a_mostrar(self.object.user.pk)
        return reverse_lazy('filtro_listar')


class Campos_defectoList(ListView):
    model = Campos_defecto
    template_name = 'validacion/filtros.html'


class Campos_defectoDelete(DeleteView):
    model = Campos_defecto
    template_name = 'validacion/eliminar_filtro.html'
    success_url = reverse_lazy('filtro_listar')
    
class img_to_show_Delete(DeleteView):
    model = img_to_show
    template_name = 'validacion/eliminar_img.html'
    success_url = reverse_lazy('login')
    

