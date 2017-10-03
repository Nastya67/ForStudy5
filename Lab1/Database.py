from Players import Players
from Commands import Commands
import pickle

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
        for i in range(len(self.commands)):
            if self.commands[i].id == command_id:
                del self.commands[i]
                break
        for pl in self.players:
            if pl.command_id == command_id:
                pl.command_id = None

    def _update_player(self, player_id, player_name, command_id):
        for i in range(len(self.players)):
            if self.players[i].id == player_id:
                self.players[i].update_name(player_name)
                if command_id  in [com.id for com in self.commands]:
                    self.players[i].command_id = command_id
                break

    def update_player(self, player):
        self._update_player(player.id, player.name, player.command_id)

    def _update_command(self, command_id, command_name, command_city):
        for i in range(len(self.commands)):
            if self.commands[i].id == command_id:
                self.commands[i].name = command_name
                self.commands[i].city = command_city
                break

    def update_command(self, command):
        self._update_command(command.id, command.name, command.city)

    def show_bestPlayers(self, n):
        if n and type(n)=="list":
            n = n[0]
        res = dict(zip([com.id for com in self.commands], [0 for i in range(len(self.commands))]))
        for pl in self.players:
            if res[pl.command_id] != 0:
                if res[pl.command_id].id < pl.id:
                    res[pl.command_id] = pl
            else:
                res[pl.command_id] = pl
        ress = []
        count = 0
        for pl in res.values():
            if pl != 0:
                ress.append(pl)
                count +=1
            if count == n:
                break
        return "\n".join(["{0} {1} {2}".format(pl.id, pl.name, self.commands.get_command(pl.command_id)) for pl in ress])

    def save(self):
        with open('players.pickle', 'wb') as f:
            pickle.dump(self.players, f)
        with open('commands.pickle', 'wb') as f:
            pickle.dump(self.commands, f)

    def load(self):
        with open('players.pickle', 'rb') as f:
            self.players = pickle.load(f)
        with open('commands.pickle', 'rb') as f:
            self.commands = pickle.load(f)

    def __str__(self):
        return "\n".join(["{0} {1} {2}".format(pl.id, pl.name, self.commands.get_command(pl.command_id)) for pl in self.players])