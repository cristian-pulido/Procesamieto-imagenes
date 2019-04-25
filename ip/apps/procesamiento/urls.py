from django.conf.urls import url


from django.urls import path
from django.views.generic import TemplateView

from apps.procesamiento.views import TaskgroupCreate, TaskgroupUpdate, TaskgroupList, TaskgroupDelete, PipelineCreate, PipelineUpdate, PipelineDelete, Multi, resultados_list


urlpatterns = [
	path('grupos/crear', TaskgroupCreate.as_view(), name='grupo_crear'),
	path('grupos/editar/<int:pk>/', TaskgroupUpdate.as_view(), name='grupo_editar'),
	path('grupos/listar/', TaskgroupList.as_view(), name='grupo_listar'),
	path('grupos/eliminar/<int:pk>/', TaskgroupDelete.as_view(), name='grupo_eliminar'),    
	path('pipeline/crear', PipelineCreate.as_view(), name='pipeline_crear'),
	path('pipeline/editar/<int:pk>/', PipelineUpdate.as_view(), name='pipeline_editar'),  
	path('pipeline/eliminar/<int:pk>/', PipelineDelete.as_view(), name='pipeline_eliminar'),    
	url(r'^multi_run',Multi,name="multi_run"),

	path('resultados/<int:pk>', resultados_list.as_view(), name='resultados'),    
    
]