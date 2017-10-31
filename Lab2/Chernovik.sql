SELECT Winner, Loser, Score, type, time AS Date, CONCAT(Name,' ',Surname) AS JudgeName, 
					CONCAT(City,', ',Street) AS Address, Comments 
                    FROM (select * from Game natural Join Judge natural join Place natural join 
                    GameResult as a inner join Result on a.idResult=Result.idResult) as a1 left join 
                    (select idGame, Name1 as Loser, Name2 as Winner from 
					(select idGame, Winner as idCommand2, CONCAT(Name,' (',City, ')') as Name2 
                    from GameResult natural join Result natural join Command) as a
                    natural join
                    (select idGame, idCommand as idCommand1, CONCAT(Name,' (',City, ')') as Name1 
                    from Game natural join GameCommand natural join Command where
                    not exists (
					select idGame, Winner as idCommand1 from GameResult natural join Result)) as b) as bb 
                    on a1.idGame=bb.idGame;

select * from Game natural Join Judge natural join Place natural join 
                    GameResult as a inner join Result on a.idResult=Result.idResult;
select idGame, Name1 as Loser, Name2 as Winner from 
					(select idGame, Winner as idCommand2, CONCAT(Name,' (',City, ')') as Name2 
                    from GameResult natural join Result as gr inner join Command on gr.Winner=Command.idCommand)
                    as w inner join
                    (select idGame, idCommand as idCommand1, CONCAT(Name,' (',City, ')') as Name1 
                    from Game natural join GameCommand natural join Command where
                    not exists (
					select idGame, Winner as idCommand1 from GameResult natural join Result)) as b;
                    
select idGame, idCommand as idCommand1, CONCAT(Name,' (',City, ')') as Name1
                    from Game natural join GameCommand natural join Command 
                    natural join GameResult as gr1 natural join Result as res where not exists(
                    select idGame, Time, Winner as idCommand1 from GameResult as gr natural join Result as res2
                    where gr.idGame = gr1.idGame and 
                    res2.Time=res.Time and res2.Winner=res.Winner);

select idGame, Time, Winner as idCommand1 from GameResult as gr natural join Result as res2;

select * from (select * from Game natural join GameCommand natural join Command 
                    natural join GameResult) as al inner join Result on al.idResult=Result.idResult;