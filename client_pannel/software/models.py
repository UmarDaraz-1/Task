from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class ProjectS(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image1 = models.ImageField(upload_to='media')
    image2 = models.ImageField(upload_to='static')
    image3 = models.ImageField(upload_to='static')
    deadline = models.DateTimeField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    file1 = models.FileField(upload_to='static')
    file2 = models.FileField(upload_to='static')
    file3 = models.FileField(upload_to='static')
    closed = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    auth_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username