from Book import Book
from Author import Author
from Database import Database

if __name__ == "__main__":
    a1 = Author(1, "auth1")
    a2 = Author(2, "auth2")
    b1 = Book(1, "book1", 1)
    b2 = Book(2, "book2", 1)
    b3 = Book(3, "book3", 2)

    db = Database()
    db.add_author(a1)
    db.add_author(a2)
    db.add_book(b1)
    db.add_book(b2)
    db.add_book(b3)
    print(db)
    input()
