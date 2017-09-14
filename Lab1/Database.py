from Books import Books
from Authors import Authors
class Database(object):
    books = Books()
    authors = Authors()

    def add_book(self, book):
        if book.author_id in [author.id for author in self.authors]:
            self.books.append(book)

    def add_author(self, author):
        if author.id not in [auth.id for auth in self.authors]:
            self.authors.append(author)

    def __str__(self):
        return "\n".join(["{0} {1} {2}".format(book.id, book.name, self.authors.get_author(book.author_id)) for book in self.books])