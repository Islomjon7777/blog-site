from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import Signal

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, default="user")
    userEmail = models.CharField(max_length=100, default="example@gmail.com")
    userImg = models.ImageField(upload_to='userImages/')
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

class PostlarModel(models.Model):
    post_choice = (
        ('yaxshi', 'Yaxshi'),
        ('yomon', 'Yomon'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    text = models.TextField()
    post_image = models.ImageField(upload_to='postImages/')
    turi = models.CharField(max_length=6, choices=post_choice, default='Yaxshi')
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(auto_now=True)

     
    def __str__(self):
        return self.title
    

class CommentModel(models.Model):
    post_comment = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(PostlarModel, on_delete=models.CASCADE, null=True, blank=True)
    profile  = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.post_comment
    

# SIGNAL SIGNAL SIGNAL SIGNAL SIGNAL SIGNAL SIGNAL SIGNAL SIGNAL SIGNAL
def Create_profile(sender, instance, created, **kwargs):
    print(sender, instance, created)
    if created:
        Profile.objects.create(user=instance)
    else:
        profile = Profile.objects.get(user=instance)
        profile.userEmail = instance.email
        profile.name = instance.first_name
        profile.save()

Signal.connect(post_save, Create_profile, sender=User)