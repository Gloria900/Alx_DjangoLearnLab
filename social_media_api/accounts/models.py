from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
  
     # users that this user follows
    following = models.ManyToManyField(
      "self",
      symmetrical=False,   # one-way follow (A follows B ≠ B follows A)
      related_name="followers",
      blank=True
    )

    def __str__(self):
      return self.username
