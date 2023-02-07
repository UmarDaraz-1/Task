from django.test import TestCase

# Create your tests here.
# models.py
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']

# views.py
from django.shortcuts import render, redirect
from .forms import ProjectForm

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def update_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form})

def track_project(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'track_project.html', {'project': project})

def delete_project(request, pk):
    Project.objects.get(pk=pk).delete()
    return redirect('dashboard')

def close_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.status = 'closed'
    project.save()
    return redirect('dashboard')

def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'dashboard.html', {'projects': projects})

# urls.py
from django.urls import path
from .views import create_project, update_project, track_project, delete_project, close_project, dashboard

urlpatterns = [
    path('create/', create_project, name='create_project'),
    path('update/<int:pk>/', update_project, name='update_project'),
    path('track/<int:pk>/', track_project, name='track_project'),
    path('delete/<int:pk>/', delete_project, name='delete_project'),
    path('close/<int:pk>/', close_project, name='close_project'),
    path('', dashboard, name='dashboard'),
]





###

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/')



from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'country', 'profile_picture']
        
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'country', 'profile_picture']



from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import CustomUserForm, EditProfileForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            # send verification email
            # ...
            return redirect('confirmation')
    else:
        form = CustomUserForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid login credentials"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def view_profile(request):
    return render(request, 'profile.html')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
