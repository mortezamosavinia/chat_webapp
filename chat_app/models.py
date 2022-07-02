from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField()

    def save(self):
        super().save()

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)


class ChatMessages(models.Model):
    room = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    message = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
