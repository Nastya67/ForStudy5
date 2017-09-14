class Book(object):
    def __init__(self, b_id, auth_id, b_name):
        self.id = b_id
        self.author_id = auth_id
        self.name = b_name
    def __str__(self):
        return "%d %s Author: %s\n" % (self.id, self.name, self.author_id)

class Author(object):
    def __init__(self, a_id, a_name):
        self.id = a_id
        self.name = a_name
    def __str__(self):
        return "%d %s" % (self.id, self.name)

class Authors(object):
    pass

if __name__ == "__main__":
    a = Author(1, "auth1")
    b = Book(1, 1, "book")
    print(a, b, sep="\n")
