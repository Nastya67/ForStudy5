class Books(list):
    def __str__(self):
        return "\n".join([str(book) for book in self])
