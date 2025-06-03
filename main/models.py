from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='labels')
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Label, on_delete = models.SET_NULL, null=True, blank=True, related_name='category_tasks')
    labels = models.ManyToManyField(Label, blank = True, related_name='label_tasks') #M:N relat 
    def __str__(self):
        return self.title
    
class SyncStatus(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='sync_status')
    status = models.CharField(max_length=50)
    last_synced = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.task.title} - {self.status}"

class Category(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name