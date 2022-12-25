from django.db import models

# Create your models here.
class Post(models.Model):

  title = models.CharField(max_length = 200, blank=False , default='')
  text = models.TextField(blank=False , default='')
