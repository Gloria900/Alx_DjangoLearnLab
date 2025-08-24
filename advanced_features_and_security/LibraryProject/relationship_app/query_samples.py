from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
  author = Author.objects.get(name=author_name)
  books = Book.objects.filter(author=author)
  print(f"Books by {author_name}: ")
  for book in books:
    print(f" — {book.title}")


# List all books in a library
def books_in_library(library_name):
  library = Library.objects.get(name=library_name)
  books = library.books.all()
  print(f"Books available in {library_name}: ")
  for book in books:
    print(f"{book.title}")

# Retrieve the librarian for a library
def library_librarian(library_name):
  library = Library.objects.get(name=library_name)
  librarian = Librarian.objects.get(library=library)
  print(f"The {library_name} librarian is {librarian.name}.")

# Test Sample Queries
if __name__ == "__main__":
  books_by_author('James Clear') # books by author
  books_in_library('Unical Main Library') #books in library
  library_librarian('GiftinTech') # librarian