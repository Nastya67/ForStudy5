class Players(list):
    def __str__(self):
        return "\n".join([str(player) for player in self])
