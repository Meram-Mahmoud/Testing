from django.contrib import admin

# Register your models here.
from tasks.models import Task

@admin.register(Task)
class TaskAdminView(admin.ModelAdmin):
    list_display = ('title', 'description', 'status')
