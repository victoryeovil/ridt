from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pictures/')

    groups = models.ManyToManyField('auth.Group', related_name='custom_user')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user', through='UserUserPermission', blank=True)

class UserUserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.CASCADE)


class CommonFields(models.Model):
    create_timestamp = models.DateTimeField(default=timezone.now)
    update_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Blog(CommonFields):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

class Comment(CommonFields):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text