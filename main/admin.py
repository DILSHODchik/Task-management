from django.contrib import admin

from .models import Task, Label, SyncStatus, Category
admin.site.register(Task)
admin.site.register(Label)
admin.site.register(SyncStatus)
admin.site.register(Category)
admin.site.site_header = "Task Management Admin"
admin.site.site_title = "Task Management Admin Portal"
admin.site.index_title = "Welcome to Task Management Admin Portal"

