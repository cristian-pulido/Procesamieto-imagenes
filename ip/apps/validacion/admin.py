from django.contrib import admin

# Register your models here.
from apps.validacion.models import Tipoimagenes, Tagsdicom, Campostagimg, Campos_defecto, img_to_show, Imagenesdefecto

admin.site.register(Tipoimagenes)
admin.site.register(Imagenesdefecto)
admin.site.register(Tagsdicom)
admin.site.register(Campostagimg)
admin.site.register(Campos_defecto)
admin.site.register(img_to_show)