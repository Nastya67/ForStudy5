class Book(object):
    def __init__(self, id, name, author_id):
        self.id = id
        self.name = name
        self.author_id = author_id
    def __str__(self):
        return "{0} {1} \t {2}".format(self.id, self.name, self.author_id)

