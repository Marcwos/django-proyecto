from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('university', 'Universitaria'),
        ('personal', 'Personal'),
        ('work', 'Laboral'), 
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES, default='personal')

    def __str__(self):
        return self.title

