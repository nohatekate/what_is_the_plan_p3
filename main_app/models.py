from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import User

ENVIRONMENTS = (
    ('A', 'Anywhere'),
    ('I', 'Inside'),
    ('O', 'Outside')
)
# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'group_id': self.id})
    
    class Meta:
        ordering = ['name']
    
class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    estimated_time = models.IntegerField(default=0)
    estimated_cost = models.IntegerField(default=0)
    day_of_week = models.CharField(max_length=20, default=' ')
    environment = models.CharField(max_length=1, choices=ENVIRONMENTS, default=ENVIRONMENTS[0][0], blank=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name}"