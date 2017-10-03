from Players import Players
from Commands import Commands
class Database(object):
    players = Players()
    commands = Commands()

    def add_player(self, player):
        if player.command_id in [com.id for com in self.commands]:
            self.players.append(player)

    def add_command(self, command):
        if command.id not in [com.id for com in self.commands]:
            self.commands.append(command)

    def del_player(self, player_id):
        for i in range(len(self.players)):
            if self.players[i].id == player_id:
                del self.players[i]
                break

    def del_command(self, command_id):
        print("inside")
        for i in range(len(self.commands)):
            if self.commands[i].id == command_id:
                del self.commands[i]
                break
        for pl in self.players:
            if pl.command_id == command_id:
                pl.command_id = None

    def __str__(self):
        return "\n".join(["{0} {1} {2}".format(pl.id, pl.name, self.commands.get_command(pl.command_id)) for pl in self.players])