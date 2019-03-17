from django.shortcuts import render
from django.urls import reverse_lazy
# Create your views here.

from apps.procesamiento.forms import gruposForm, PipelineForm
from apps.procesamiento.models import Taskgroup, Task, Pipeline
from apps.validacion.models import Tipoimagenes

from django.views.generic import CreateView, UpdateView, ListView, DeleteView



class TaskgroupCreate(CreateView):
	model = Taskgroup
	form_class = gruposForm
	template_name = 'procesamiento/taskgroup_form.html'

	def get_success_url(self):
		G=self.object
		orden=G.orden
		for t in orden.split('_')[:-1]:
			G.task.add(Task.objects.get(pk=int(t)))
		G.save()
        
		return reverse_lazy('grupo_listar')

class TaskgroupUpdate(UpdateView):
	model = Taskgroup
	form_class = gruposForm
	template_name = 'procesamiento/taskgroup_form.html'

	def get_success_url(self):
		G=self.object
		G.task.clear()
		orden=G.orden
		for t in orden.split('_')[:-1]:
			G.task.add(Task.objects.get(pk=int(t)))
		G.save()
        
		return reverse_lazy('grupo_listar')
    
class TaskgroupList(ListView):
	model = Taskgroup
	template_name = 'procesamiento/taskgroup_listar.html'
    
class TaskgroupDelete(DeleteView):
    model = Taskgroup
    # a donde va dirigido
    template_name = 'procesamiento/taskgroup_eliminar.html'
    def get_success_url(self):
        
        return reverse_lazy('grupo_listar')
    
class PipelineCreate(CreateView):
	model = Pipeline
	form_class = PipelineForm
	template_name = 'procesamiento/pipeline_form.html'

	def get_success_url(self):
		P=self.object
		orden=P.orden
		for t in orden.split('_')[:-1]:
			P.grupos.add(Taskgroup.objects.get(pk=int(t)))
		P.save()
        
		return reverse_lazy('grupo_listar')
    
class PipelineUpdate(UpdateView):
	model = Pipeline
	form_class = PipelineForm
	template_name = 'procesamiento/pipeline_form.html'

	def get_success_url(self):
		P=self.object
		P.grupos.clear()        
		orden=P.orden
		for t in orden.split('_')[:-1]:
			P.grupos.add(Taskgroup.objects.get(pk=int(t)))
		P.save()
        
		return reverse_lazy('grupo_listar')
    
class PipelineDelete(DeleteView):
    model = Pipeline
    # a donde va dirigido
    template_name = 'procesamiento/pipeline_eliminar.html'
    def get_success_url(self):
        
        return reverse_lazy('grupo_listar')
    