from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='labels')
    class Meta:
        ordering = ['name']  #ordering by name : Aslam, Sanjar, Javoxir, Xasan ...
        unique_together = ['name','user'] #two same name and user cant exist together cuz they are together unique 
    
    def __str__(self):
        return self.name
    
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low','LOW'),
        ('mid','MEDIUM'),
        ('high','HIGH'),
        ('urg','URGENT'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length = 10, choices = PRIORITY_CHOICES, default = 'medium')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    completed_at = models.DateTimeField(null = True, blank = True)
    
    #here ralationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    labels = models.ManyToManyField(Label, blank = True, related_name='label_tasks') #M:N relationship
    
    #integration with google
    google_event_id = models.CharField(max_length=255, blank=True, null=True)
    sync_with_calendar = models.BooleanField(default=True)
    
    def save(self,*args, **kwargs):
        if self.is_completed == True and self.completed_at:
            completed_at = timezone.now
        elif self.is_completed == False:
            completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if not self.is_completed and self.due_date:
            return timezone.now() > self.due_date
        return False
        
    
    @property
    def days_until_due(self):
        if not self.is_completed and self.due_date:
            return (self.due_date.date() - timezone.now().date()).days
        return None

    
    
    def complete_task(self):
        self.is_completed = True 
        self.completed_at = timezone.now()
        self.save()
        return self
        
    #if you want reset and todo task again
    def reopen_task(self):
        self.is_completed = False
        self.completed_at = None
        self.save()
        return self
        
    def __str__(self):
        return self.title
    
class SyncStatus(models.Model):
    SYNC_STATUS = [
        ('pending','Pending'),
        ('synced','Synced'),
        ('failed',"Failed"),
        ('manual','do it mannual'),
    ]
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='sync_status')
    status = models.CharField(max_length=50, choices = SYNC_STATUS, default = 'pending')
    last_synced = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank = True)
    syncs_attempts = models.PositiveIntegerField(default= 0)
    
    
    def __str__(self):
        return f"{self.task.title} - {self.status}"
    
    def sync_success(self):
        self.status = 'synced'
        self.error_message = ''
        self.syncs_attempts = 0
        self.save()
        return self
    
    def sync_failed(self, error_msg):
        self.status = 'failed'
        self.error_message = error_msg
        self.syncs_attempts += 1 
        self.save()
        return self
        
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    google_calendar_id = models.CharField(max_length=255, blank=True)
    auto_sync_enabled = models.BooleanField(default=True)
    default_task_priority = models.CharField(max_length=10, 
        choices= Task.PRIORITY_CHOICES, default= 'medium')
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}`s profile "
    

