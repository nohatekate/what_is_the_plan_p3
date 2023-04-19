from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    name = models.CharField(),
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ideas = models.ForeignKey(Idea), 
    # crew = models.ManyToManyField(user),
    icon = models.ImageField(), 


