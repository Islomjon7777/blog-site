from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'userEmail', 'userImg']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['post_comment']
