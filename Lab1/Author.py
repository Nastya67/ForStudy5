class Author(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self):
        return "{0} {1}".format(self.id, self.name)

