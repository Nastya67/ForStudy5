import pickle
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
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
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
        finally:
            self.connection.close()
        return res

    def delRow(self, idGame, Time):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = """delete from GameResult where 
                idResult in (select idResult from Result where Time=%s) 
                    and idGame=%s;"""
                cursor.execute(sql, (Time, idGame))
        finally:
            self.connection.commit()


    def load(self):
        pass

    def __str__(self):
        return
