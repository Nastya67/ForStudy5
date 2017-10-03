class Player(object):
    def __init__(self, id, name, command_id):
        self.id = id
        self.name = name
        self.command_id = command_id
    def __str__(self):
        return "{0} {1} \t {2}".format(self.id, self.name, self.command_id)

