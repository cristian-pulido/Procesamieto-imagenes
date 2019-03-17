from django.conf.urls import url


from django.urls import path


from apps.procesamiento.views import TaskgroupCreate, TaskgroupUpdate, TaskgroupList, TaskgroupDelete, PipelineCreate, PipelineUpdate, PipelineDelete


urlpatterns = [
	path('grupos/crear', TaskgroupCreate.as_view(), name='grupo_crear'),
	path('grupos/editar/<int:pk>/', TaskgroupUpdate.as_view(), name='grupo_editar'),
	path('grupos/listar/', TaskgroupList.as_view(), name='grupo_listar'),
	path('grupos/eliminar/<int:pk>/', TaskgroupDelete.as_view(), name='grupo_eliminar'),    
	path('pipeline/crear', PipelineCreate.as_view(), name='pipeline_crear'),
	path('pipeline/editar/<int:pk>/', PipelineUpdate.as_view(), name='pipeline_editar'),  
	path('pipeline/eliminar/<int:pk>/', PipelineDelete.as_view(), name='pipeline_eliminar'),    
    
]