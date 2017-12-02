import json
import random
import pymysql.cursors

class Database(object):
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='070698yfcnz97',
                                     db='Lab2',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

    def selectGames(self):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select g.idGame, r.Time, r.Score, CONCAT(Command.Name,' (',Command.City, ')') as Winner, 
                l.Loser, g.time as Date, CONCAT(j.Name,' ',j.Surname) AS JudgeName, 
                CONCAT(p.City,', ',Street) AS Address, Comments 
                from Game g natural join GameResult gr 
                inner join Result r on gr.idResult=r.idResult 
                inner join Command on Command.idCommand=r.Winner 
                inner join Judge j on g.idJudge=j.idJudge
                inner join Place p on p.idPlace=g.idPlace
                inner join (
                select res.idGame, Command.idCommand, res.Time, CONCAT(Command.Name,' (',Command.City, ')') as Loser 
                from Command 
                inner join (
                select g1.idGame, gc1.idCommand, r1.Time from Game g1 natural join GameCommand gc1 
                inner join GameResult gr1 on g1.idGame=gr1.idGame 
                inner join Result r1 on gr1.idResult=r1.idResult where not exists(
                select g2.idGame, r2.Winner as idCommand, r2.Time from Game g2 natural join GameResult gr2 
                inner join Result r2 on gr2.idResult=r2.idResult 
                where g1.idGame=g2.idGame and gc1.idCommand=r2.Winner and r1.Time=r2.Time)) 
                as res on Command.idCommand=res.idCommand)as l on l.idGame=g.idGame 
                where l.Time=r.Time;"""
            cursor.execute(sql, ())
            res = cursor.fetchall()
        return res
    def selectGamesWhereJ(self, judge):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select g.idGame, r.Time, r.Score, CONCAT(Command.Name,' (',Command.City, ')') as Winner, 
                        l.Loser, g.time as Date, CONCAT(j.Name,' ',j.Surname) AS JudgeName, 
                        CONCAT(p.City,', ',Street) AS Address, Comments 
                        from Game g natural join GameResult gr 
                        inner join Result r on gr.idResult=r.idResult 
                        inner join Command on Command.idCommand=r.Winner 
                        inner join Judge j on g.idJudge=j.idJudge
                        inner join Place p on p.idPlace=g.idPlace
                        inner join (
                        select res.idGame, Command.idCommand, res.Time, CONCAT(Command.Name,' (',Command.City, ')') as Loser 
                        from Command 
                        inner join (
                        select g1.idGame, gc1.idCommand, r1.Time from Game g1 natural join GameCommand gc1 
                        inner join GameResult gr1 on g1.idGame=gr1.idGame 
                        inner join Result r1 on gr1.idResult=r1.idResult where not exists(
                        select g2.idGame, r2.Winner as idCommand, r2.Time from Game g2 natural join GameResult gr2 
                        inner join Result r2 on gr2.idResult=r2.idResult 
                        where g1.idGame=g2.idGame and gc1.idCommand=r2.Winner and r1.Time=r2.Time)) 
                        as res on Command.idCommand=res.idCommand)as l on l.idGame=g.idGame 
                        where l.Time=r.Time and j.isMan=%s;"""
            cursor.execute(sql, (judge))
            res = cursor.fetchall()
        return res
    def selectGamesWhereD(self, date0, date1):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select g.idGame, r.Time, r.Score, CONCAT(Command.Name,' (',Command.City, ')') as Winner, 
                        l.Loser, g.time as Date, CONCAT(j.Name,' ',j.Surname) AS JudgeName, 
                        CONCAT(p.City,', ',Street) AS Address, Comments 
                        from Game g natural join GameResult gr 
                        inner join Result r on gr.idResult=r.idResult 
                        inner join Command on Command.idCommand=r.Winner 
                        inner join Judge j on g.idJudge=j.idJudge
                        inner join Place p on p.idPlace=g.idPlace
                        inner join (
                        select res.idGame, Command.idCommand, res.Time, CONCAT(Command.Name,' (',Command.City, ')') as Loser 
                        from Command 
                        inner join (
                        select g1.idGame, gc1.idCommand, r1.Time from Game g1 natural join GameCommand gc1 
                        inner join GameResult gr1 on g1.idGame=gr1.idGame 
                        inner join Result r1 on gr1.idResult=r1.idResult where not exists(
                        select g2.idGame, r2.Winner as idCommand, r2.Time from Game g2 natural join GameResult gr2 
                        inner join Result r2 on gr2.idResult=r2.idResult 
                        where g1.idGame=g2.idGame and gc1.idCommand=r2.Winner and r1.Time=r2.Time)) 
                        as res on Command.idCommand=res.idCommand)as l on l.idGame=g.idGame 
                        where l.Time=r.Time and g.time >= %s and g.time <= %s;"""
            cursor.execute(sql, (date0, date1))
            res = cursor.fetchall()
        return res
    def delRow(self, idGame, Time):
        try:
            with self.connection.cursor() as cursor:
                sql = """delete from GameResult where 
                idResult in (select idResult from Result where Time=%s) 
                    and idGame=%s;"""
                cursor.execute(sql, (Time, idGame))
                sql = """select count(*) as num from GameResult where idGame=%s"""
                cursor.execute(sql, (idGame,))
                num = cursor.fetchone()['num']
                if num == 0:
                    sql = """delete from Game where idGame=%s"""
                    cursor.execute(sql, (idGame,))
        except:
            pass
        else:
            self.connection.commit()
    def selectCommands(self):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(Name,' (',City, ')') as command from Command"""
            cursor.execute(sql, ())
            res = cursor.fetchall()
        return res
    def selectCommandsWhere(self, idGame):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(Name,' (',City, ')') as command from Command
                    where idCommand in (select idCommand from Game natural join GameResult where idGame=%s)"""
            cursor.execute(sql, (idGame))
            res = cursor.fetchall()
        return res
    def selectJudges(self):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(Name, ' ', Surname) as judge from Judge"""
            cursor.execute(sql, ())
            res = cursor.fetchall()
        return res
    def selectAddress(self):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(City,', ',Street) as address from Place"""
            cursor.execute(sql, ())
            res = cursor.fetchall()
        return res
    def selectDateWhere(self, idGame):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select time, comments from Game where idGame=%s"""
            cursor.execute(sql, (idGame))
            res = cursor.fetchone()
        return res['time'], res['comments']
    def selectScoreWhere(self, idGame, Time):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select score from Game natural join GameResult gr 
                    inner join Result r on gr.idResult=r.idResult where idGame=%s and r.Time=%s"""
            cursor.execute(sql, (idGame, Time))
            res = cursor.fetchone()
        return res['score']
    def selectLoser(self, idGame, Time):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(c.Name,' (',c.City, ')') as Loser 
                    from Command c
                    inner join (
					select g1.idGame, gc1.idCommand, r1.Time from Game g1 natural join GameCommand gc1 
                    inner join GameResult gr1 on g1.idGame=gr1.idGame 
                    inner join Result r1 on gr1.idResult=r1.idResult where not exists(
                    select g2.idGame, r2.Winner as idCommand, r2.Time from Game g2 natural join GameResult gr2 
                    inner join Result r2 on gr2.idResult=r2.idResult 
                    where g1.idGame=g2.idGame and gc1.idCommand=r2.Winner and r1.Time=r2.Time)) 
                    as res on c.idCommand=res.idCommand where res.idGame=%s and res.Time=%s"""
            cursor.execute(sql, (idGame, Time))
            res = cursor.fetchone()
        return res['Loser']
    def selectWinner(self, idGame, Time):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(c.Name,' (',c.City, ')') as Winner 
                    from Command c 
                    inner join Result r on c.idCommand=r.Winner
                    inner join GameResult gr on gr.idResult=r.idResult
                    inner join Game g on gr.idGame=g.idGame where g.idGame=%s and r.Time=%s"""
            cursor.execute(sql, (idGame, Time))
            res = cursor.fetchone()
        return res['Winner']
    def selectJudgeWhere(self, idGame):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(Name,' ',Surname) AS JudgeName 
                    from Game natural join Judge where idGame=%s"""
            cursor.execute(sql, (idGame))
            res = cursor.fetchone()
        return res['JudgeName']
    def selectAddressWhere(self, idGame):
        res = {}
        with self.connection.cursor() as cursor:
            sql = """select CONCAT(City,', ',Street) AS Address 
                    from Game natural join Place where idGame=%s"""
            cursor.execute(sql, (idGame))
            res = cursor.fetchone()
        return res['Address']
    def selectSpecial(self):

    def updateDate(self, idGame, Date):
        with self.connection.cursor() as cursor:
            sql = """update Game SET time=%s where idGame=%s"""
            cursor.execute(sql, (Date, idGame))
        self.connection.commit()
    def updateScore(self, idGame, Time, Score):
        with self.connection.cursor() as cursor:
            sql = """update Result SET Score=%s where Time=%s and idResult in 
                    (select idResult from Game natural join GameResult where idGame=%s)"""
            cursor.execute(sql, (Score, Time, idGame))
        self.connection.commit()
    def updateComment(self, idGame, Comment):
        with self.connection.cursor() as cursor:
            sql = """update Game SET Comments=%s where idGame=%s"""
            cursor.execute(sql, (Comment, idGame))
        self.connection.commit()
    def updateAddress(self, idGame, Address):
        with self.connection.cursor() as cursor:
            idPlace = self.getAddressId(Address)
            sql = """update Game Set idPlace=%s where idGame=%s"""
            cursor.execute(sql, (idPlace, idGame))
        self.connection.commit()
    def updateJudge(self, idGame, Judge):
        with self.connection.cursor() as cursor:
            idJudge = self.getJudgeId(Judge)
            sql = """update Game Set idJudge=%s where idGame=%s"""
            cursor.execute(sql, (idJudge, idGame))
        self.connection.commit()
    def updateWinner(self, idGame, Time, Winner):
        with self.connection.cursor() as cursor:
            idCommand = self.getCommandId(Winner)
            sql = """update Result Set Winner=%s where Time=%s and idResult in (select idResult from 
                    Game g natural join GameResult gr
                    where g.idGame=%s);"""
            cursor.execute(sql, (idCommand, Time, idGame))
        self.connection.commit()

    def insertGame(self, game):
        try:
            idJudge = self.getJudgeId(game['Judge'])
            idAddress = self.getAddressId(game['Address'])
            Winner = self.getCommandId(game['Winner'])
            Loser = self.getCommandId(game['Loser'])
            with self.connection.cursor() as cursor:
                sql = """insert into Game values (%s, 'Friendly', %s, %s, %s, %s)"""
                cursor.execute(sql, (game['idGame'], game['Date'], game['Comments'], idAddress, idJudge))
                sql = """insert into Result values (%s, %s, %s, %s)"""
                idResult = self.generateId()
                cursor.execute(sql, (idResult, game['Time'], game['Score'], Winner))
                sql = """insert into GameResult values (%s, %s, %s)"""
                gr = self.generateId()
                cursor.execute(sql, (gr, game['idGame'], idResult))
                sql = """insert into GameCommand values (%s, %s, %s)"""
                gc = self.generateId()
                cursor.execute(sql, (gc, Winner,  game['idGame']))
                gc = self.generateId()
                cursor.execute(sql, (gc, Loser, game['idGame']))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return "OK"
    def insertTime(self, game):
        try:
            Winner = self.getCommandId(game['Winner'])
            with self.connection.cursor() as cursor:
                sql = """select count(*) as num from Result where Time=%s and idResult in(
                        select idResult from GameResult where idGame=%s)"""
                cursor.execute(sql, (game['Time'], game['idGame']))
                num = cursor.fetchone()['num']
                if num > 0:
                    raise Exception("In Game %s time %s was exist"%(game['Time'], game['idGame']))
                sql = """insert into Result values (%s, %s, %s, %s)"""
                idResult = self.generateId()
                cursor.execute(sql, (idResult, game['Time'], game['Score'], Winner))
                sql = """insert into GameResult values (%s, %s, %s)"""
                gr = self.generateId()
                cursor.execute(sql, (gr, game['idGame'], idResult))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return "OK"
    def insertCommand(self, command):
        try:
            with self.connection.cursor() as cursor:
                sql = """insert into Command values (%s, %s, %s)"""
                cursor.execute(sql, (command['idCommand'], command['City'], command['Name']))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return "OK"
    def insertJudge(self, judge):
        try:
            with self.connection.cursor() as cursor:
                sql = """insert into Judge values (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (judge['idJudge'], judge['Exp'], judge['Name'],
                                     judge['Surname'], judge["Age"], judge["isMan"]))
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return "OK"
    def insertAddress(self, address):
        try:
            with self.connection.cursor() as cursor:
                sql = """insert into Place values (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (address['idPlace'], address['Country'], address['City'],
                                     address['Street'], address["Hall"], address["Field"]))
            self.connection.commit()
        except Exception as e:
            print("exception", e)
            return e
        else:
            return "OK"

    def dropAll(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """delete from GameResult;"""
                cursor.execute(sql, ())
                sql = """delete from Result;"""
                cursor.execute(sql, ())
                sql = """delete from GameCommand;"""
                cursor.execute(sql, ())
                sql = """delete from Command;"""
                cursor.execute(sql, ())
                sql = """delete from Game;"""
                cursor.execute(sql, ())
                sql = """delete from Judge;"""
                cursor.execute(sql, ())
                sql = """delete from Place;"""
                cursor.execute(sql, ())
            self.connection.commit()
        except Exception as e:
            return e
        else:
            return "OK"

    def conClose(self):
        self.connection.close()

    def load(self):
        self.dropAll()
        pref=r'D:\Nastya\Учеба\3курс\DB\ForStudy5\Lab2\app\Data'
        Commands = json.load(open(pref+r'\Command.json'))['Commands']
        Judges = json.load(open(pref+r"\Judge.json"))['Judges']
        Address = json.load(open(pref+r"\Address.json"))['Address']
        for com in Commands:
            self.insertCommand(com)
        for judge in Judges:
            self.insertJudge(judge)
        for adr in Address:
            self.insertAddress(adr)

    def getJudgeId(self, Judge):
        res = 0
        with self.connection.cursor() as cursor:
            sql = """select idJudge from Judge where Name=%s and Surname=%s"""
            Name, Surname = Judge.split(" ")
            cursor.execute(sql, (Name, Surname))
            res = cursor.fetchone()['idJudge']
        return res
    def getCommandId(self, Command):
        res = 0
        with self.connection.cursor() as cursor:
            name, city = Command.replace("(", '').replace(")", "").split(" ")
            sql = """select idCommand from Command where Name=%s and City=%s"""
            cursor.execute(sql, (name, city))
            res = cursor.fetchone()['idCommand']
        return res
    def getAddressId(self, Address):
        res = 0
        with self.connection.cursor() as cursor:
            sql = """select idPlace from Place where City=%s and Street=%s"""
            City, Street = Address.split(", ")
            cursor.execute(sql, (City, Street))
            res = cursor.fetchone()['idPlace']
        return res

    def generateId(self):
        return random.randint(3, 100)

    def __str__(self):
        return
