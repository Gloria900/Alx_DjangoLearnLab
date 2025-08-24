from django.db import models

# Author model has only a name field
class Author(models.Model):
  name = models.CharField(max_length=255)

# Book model has title, publication_year and author fields. author field uses a FK to link to the Author model
class Book(models.Model):
  title = models.CharField(max_length=255)
  publication_year = models.IntegerField()
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
