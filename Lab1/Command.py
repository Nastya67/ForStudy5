class Command(object):
    def __init__(self, id, name, city):
        self.id = id
        self.name = name
        self.city = city
    def __str__(self):
        return "{0} {1} {2}".format(self.id, self.name, self.city)

