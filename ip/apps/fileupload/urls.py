# encoding: utf-8
from django.urls import path
from apps.fileupload.views import PictureCreateView, PictureDeleteView, PictureListView, PictureView, PictureViewImg, Select

urlpatterns = [
    path('new/', PictureCreateView.as_view(), name='upload-new'),
    path('delete/<int:pk>', PictureDeleteView.as_view(), name='upload-delete'),
    #path('view/', PictureListView.as_view(), name='upload-view'),
    path('informacion/<slug:pk>', PictureView.as_view(), name='picture'),
    path('visor/<slug:pk>', PictureViewImg.as_view(), name='img_to_show'),
    path('select/<slug:pk>',Select,name="select"),
    
]
