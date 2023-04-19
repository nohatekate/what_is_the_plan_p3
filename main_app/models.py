from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'group_id': self.id})