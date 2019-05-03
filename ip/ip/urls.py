"""ip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views
from django.views.generic import TemplateView

from .views import reportes, lista, carga, run_pipeline

urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path('', lambda x: HttpResponseRedirect('/login')),
    path('report_builder/', include('report_builder.urls'),name="reports"),

    url(r'^login/$', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^accounts/logout/$', views.LogoutView.as_view(template_name='registration/logout.html'),name='logout'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^reportes$',reportes,name="reportes"),

    url(r'^lista$',lista,name="lista"),

    url(r'^upload$',carga,name="carga"), 

    path('registro/', include('apps.fileupload.urls')),
    path('validacion/', include('apps.validacion.urls')),

    path('procesamiento/', include('apps.procesamiento.urls')),
    
    url(r'^visualizador', TemplateView.as_view(template_name='slicedrop/index.html'), name="visor"),
    
    path('script/run_pipeline/<int:user_pk>/<int:config_pk>/', run_pipeline, name='run_pipeline'),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)