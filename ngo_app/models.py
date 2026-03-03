from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User

class NGO(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    # add other NGO fields if needed

    def __str__(self):
        return self.name

class NGOMedia(models.Model):
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ngo_media/', null=True, blank=True)
    video = models.FileField(upload_to='ngo_media/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.ngo.name}"
