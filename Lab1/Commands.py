class Commands(list):
    def __str__(self):
        return "\n".join([str(command) for command in self])
    def get_command(self, id):
        for el in self:
            if el.id == id:
                return el