from bookshelf.models import Book

# Create a Book instance

new_book = Book.objects.create(title='George Orwell', author='Nineteen Eighty-Four', publication_year=1984)

# Expected output for print(new_book): Book object (1)
