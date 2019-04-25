from django.contrib import admin




# Register your models here.
from apps.procesamiento.models import Task, Taskgroup, Pipeline, task_celery, results, default_result

admin.site.register(Task)
admin.site.register(Taskgroup)
admin.site.register(Pipeline)
admin.site.register(task_celery)
admin.site.register(results)
admin.site.register(default_result)