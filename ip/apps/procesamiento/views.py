from django.shortcuts import render,redirect
from django.urls import reverse_lazy
# Create your views here.

from apps.procesamiento.forms import gruposForm, PipelineForm, MultiForm, configForm
from apps.procesamiento.models import Taskgroup, Task, Pipeline, task_celery, config
from apps.validacion.models import Tipoimagenes, Imagenesdefecto, img_to_show
from apps.fileupload.models import Picture


from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from ip.views import run_pipeline



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
    
def Multi(request):
    
    form = MultiForm()
    
    if request.method == "POST":
        form = MultiForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user_pk=data['user']
            lista=data['lista_img']
            p_pk=data['pipeline_pk']
            imgs=lista.split('_')[:-1]
            for img in imgs:
                run_pipeline(request,user_pk,img,p_pk)
            
            
            
        form = MultiForm()
        return render(request, 'procesamiento/multi.html', {'form': form})
    
    if request.method == "GET":
        form = MultiForm()
    
    return render(request, 'procesamiento/multi.html', {'form': form})

def configView(request,pk_imagen,pk_pipe,pk_tipo):
    
    form = configForm()
    
    img=Picture.objects.get(pk=pk_imagen)
    pipe=Pipeline.objects.get(pk=pk_pipe)
    tipo=Imagenesdefecto.objects.get(pk=pk_tipo)
    
    context={
      'img':img,
      'form': form,
      'pipe':pipe,  
      'tipo':tipo,  
    }
    
    if request.method == "POST":
        form = configForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            pipeline_pk=data['pipeline_pk']
            imagen_pk=data['imagen_pk']
            lista=data['entradas']
            
            if pipe.tipo_imagen.nombre != 'DWI':
            
                tipo_pk, t1_pk = lista.split(',')[:-1]
            
                n=len(config.objects.filter(entradas=(tipo_pk,t1_pk)))
                
            else:
                tipo_pk = lista.split(',')[:-1][0]
                
                n=len(config.objects.filter(entradas=tipo_pk))
            
            if n == 0 :
                c=config.objects.create(pipeline=pipe,imagen=img)
                if pipe.tipo_imagen.nombre != 'DWI':
                    c.entradas.add(tipo_pk,t1_pk)
                else:
                    c.entradas.add(tipo_pk)
                c.save()
                return redirect('picture',pk=pk_imagen)
            
            else:
                error = "Ya existe esta Configuración"
                context['error']=error
            
                form = configForm()
                return render(request, 'procesamiento/config.html', context)
    
    if request.method == "GET":
        form = configForm()
    
    return render(request, 'procesamiento/config.html', context)

    
class resultados_list(DetailView):
	model = task_celery
	template_name = 'procesamiento/resultados.html'

    
    

    
       
  
    