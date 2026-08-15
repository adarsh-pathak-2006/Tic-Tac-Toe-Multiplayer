from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    bio=models.TextField(null=True)
    profile_pic=models.ImageField(upload_to='pfps/', null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name=f"{self.user.first_name} {self.user.last_name}"
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

