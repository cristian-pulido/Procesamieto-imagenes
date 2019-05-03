from django.urls import path

from apps.validacion.views import Campos_defectoCreate, Campos_defectoList, Campos_defectoUpdate, Campos_defectoDelete, img_to_show_Delete

urlpatterns = [


    path('nuevo', Campos_defectoCreate.as_view(), name='filtro_crear'),
    path('editar/<int:pk>/', Campos_defectoUpdate.as_view(), name='filtro_editar'),
    path('filtros/', Campos_defectoList.as_view(), name='filtro_listar'),
    path('eliminar/<int:pk>/', Campos_defectoDelete.as_view(), name='filtro_eliminar'),
    path('eliminar_img/<int:pk>/', img_to_show_Delete.as_view(), name='img_eliminar'),

]