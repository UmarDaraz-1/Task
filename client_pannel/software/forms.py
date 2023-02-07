from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectS
        fields = '__all__'



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'country', 'profile_pic']
        