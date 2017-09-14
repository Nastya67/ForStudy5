class Authors(list):
    def __str__(self):
        return "\n".join([str(author) for author in self])
    def get_author(self, id):
        for el in self:
            if el.id == id:
                return el