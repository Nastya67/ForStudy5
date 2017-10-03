from Player import Player
from Command import Command
from Database import Database
import re
import os
import time

def get_list(command, startStr):
    res = []
    elems = command[len(startStr+" ("):].split("), (")
    for p in elems:
        if p:
            fields = p.replace(")", "").split(", ")
            if fields:
                res.append(fields)
    return res

def getPlayers(command):
    tmp = get_list(command, "create player")
    res = []
    for el in tmp:
        res.append(Player(int(el[0]), el[1], int(el[2])))
    return res

def getCommands(command):
    tmp = get_list(command, "create command")
    res = []
    for el in tmp:
        res.append(Command(int(el[0]), el[1], el[2]))
    return res

def getIds(command):
    res = []
    ids = ""
    startStrings = ["delete player", "delete command"]
    for ss in startStrings:
        if command.startswith(ss):
            ids = command[len(ss):].strip()
            break
    elems = ids.split(", ")
    for el in elems:
        if el:
            res.append(int(el))
    return res

def getDataToUpdate(command):
    res = []
    data = ""
    startStrings = ["update player", "update command"]
    isPlayer = None
    for i in range(len(startStrings)):
        if command.startswith(startStrings[i]):
            data = command[len(startStrings[i]):].strip()
            isPlayer = bool(i)
            break
    elems = data.split(" ")
    for el in elems:
        if el:
            res.append(el.replace("(", "").replace(")", "").replace(",", ""))
    if isPlayer == False:
        return [Player(int(res[0]), res[1], int(res[2]))]
    if isPlayer == True:
        return [Command(int(res[0]), res[1], res[2])]
    return None

def getCount(command:str):
    return [int(re.findall(r"(\d+)", command)[0])]

if __name__ == "__main__":
    c1 = Command(1, "com1", "city1")
    c2 = Command(2, "com2", "city2")
    p1 = Player(1, "pl1", 1)
    p2 = Player(2, "pl2", 1)
    p3 = Player(3, "pl3", 2)

    db = Database()
    db.add_command(c1)
    db.add_command(c2)
    db.add_player(p1)
    db.add_player(p2)
    db.add_player(p3)
    dict_create = {r"create player (\(\d+, \w+, \d+\), )*\(\d+, \w+, \d+\)": {"funk":db.add_player, "args":getPlayers},
                   r"create command (\(\d+, \w+, \w+\), )*\(\d+, \w+, \w+\)": {"funk":db.add_command, "args":getCommands}}
    dict_delete = {r"delete player (\d+, )*\d+": {"funk":db.del_player, "args":getIds},
                   r"delete command (\d+, )*\d+": {"funk": db.del_command, "args": getIds}}
    dict_update = {r"update player \d+ \(\w+, \d+\)": {"funk":db.update_player, "args":getDataToUpdate},
                   r"update command \d+ \(\w+, \w+\)": {"funk":db.update_command, "args":getDataToUpdate}}
    dict_show = {r"show \d+ best player(s)?": {"funk":db.show_bestPlayers, "args":getCount}}
    command_dict = {"creat": dict_create,
                    "delet": dict_delete,
                    "updat": dict_update,
                    "show ": dict_show}
    additionalInfo = ""
    while(True):
        os.system('cls')
        print(db)
        print("-----------")
        print(additionalInfo)
        additionalInfo = ""
        command = input()
        command = command.lower().strip()
        if not command:
            continue
        if not command_dict.get(command[:5]):
            additionalInfo = "Wrong command"
            continue
        category = command_dict[command[:5]]
        if category:
            for k, v in category.items():
                if re.match(k, command):
                    for elem in v["args"](command):
                        additionalInfo = v["funk"](elem)
                    break

#update player 1 (player1, 1)
#update command 1 (command1, c1)
#show 1 best players