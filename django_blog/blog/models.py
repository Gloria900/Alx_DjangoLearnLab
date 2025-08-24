from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200) # Post title
  content = models.TextField() # Post content
  published_date = models.DateTimeField(auto_now_add=True) # Set post date when created
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post') # Link to the User model
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  tags = TaggableManager()
  
  def __str__(self):
    return self.title # Display name in admin and shell
  
   # Handy for redirects after create/update/delete (used by CBVs and templates)
  def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
  
class Comment(models.Model):
  # Link each comment to a specific blog post
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  # Link each comment to the user who wrote it
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  # The actual comment text
  content = models.TextField()
  # Auto-set when comment is created
  created_at = models.DateTimeField(auto_now_add=True)
  # Auto-set when comment is updated
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f'Comment by {self.author} on {self.post}'