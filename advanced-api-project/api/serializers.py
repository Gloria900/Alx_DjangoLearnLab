from rest_framework import serializers
from datetime import date
from .models import Book, Author

# Serializes the Book model
class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__' # Shows all fields in the model

  # Validate publication_year to ensure it's not in the future
  def validate_publication_year(self, data):
    if data['publication_year'] >  date.today().year:
      raise serializers.ValidationError("Publication year cannot be in the future.")
    return data

# Serializes the Author model
class AuthorSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=255)
  books = BookSerializer(many=True, read_only=True) # Dynamically serialize all books related to this author

  class Meta:
    model = Author
    fields = ['name', 'books']