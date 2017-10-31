show databases;



-- MySQL Script generated by MySQL Workbench

-- Tue Oct 24 20:17:34 2017

-- Model: New Model    Version: 1.0

-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, 
UNIQUE_CHECKS=0;

SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHCREATE TABLE IF NOT EXISTS `Lab2`.`Place` (
  `idPlace` INT NOT NULL,
  `Country` VARCHAR(45) NULL,
  `City` VARCHAR(45) NULL,
  `Street` VARCHAR(45) NULL,
  `Hall` INT NULL,
  `Field` INT NULL,
  PRIMARY KEY (`idPlace`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Lab2`.`Judge` (
  `idJudge` INT NOT NULL,
  `Experience` INT NULL,
  `Name` VARCHAR(45) NULL,
  `Surname` VARCHAR(45) NULL,
  `Age` INT NULL,
  PRIMARY KEY (`idJudge`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Lab2`.`Game` (
  `idGame` INT NOT NULL,
  `type` VARCHAR(45) NULL,
  `time` DATETIME NULL,
  `Comments` TEXT NULL,
  `idPlace` INT,
  `idJudge` INT,
  PRIMARY KEY (`idGame`),
  FOREIGN KEY (`idPlace`)
    REFERENCES `Lab2`.`Place` (`idPlace`),
  FOREIGN KEY (`idJudge`)
    REFERENCES `Lab2`.`Judge` (`idJudge`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Lab2`.`Command` (
  `idCommand` INT NOT NULL,
  `City` VARCHAR(45) NULL,
  `Name` VARCHAR(45) NULL,
  PRIMARY KEY (`idCommand`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Lab2`.`GameCommand` (
  `idGameCommand` INT NOT NULL,
  `idCommand` INT,
  `idGame` INT,
  PRIMARY KEY (`idGameCommand`),
  FOREIGN KEY (`idCommand`)
    REFERENCES `Lab2`.`Command` (`idCommand`),
  FOREIGN KEY (`idGame`)
    REFERENCES `Lab2`.`Game` (`idGame`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Lab2`.`Result` (
  `idResult` INT NOT NULL,
  `Time` INT NULL,
  `Score` VARCHAR(10) NULL,
  `Winner` INT,
  PRIMARY KEY (`idResult`),
  FOREIGN KEY (`Winner`)
    REFERENCES `Lab2`.`Command` (`idCommand`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Lab2`.`GameResult` (

  `idGameResult` INT NOT NULL,
  `idGame` INT,
  `idResult` INT,
  PRIMARY KEY (`idGameResult`),
  FOREIGN KEY (`idGame`)
    REFERENCES `Lab2`.`Game` (`idGame`),
  FOREIGN KEY (`idResult`)
    REFERENCES `Lab2`.`Result` (`idResult`))
ENGINE = InnoDB;




SELECT Winner, Loser, Score, type, time AS Date, CONCAT(Name,' ',Surname) AS JudgeName, 
					CONCAT(City,', ',Street) AS Address, Comments 
                    FROM (Game natural Join Judge natural join Place natural join 
                    GameResult natural join Result) natural join 
                    (select idGame, Name1 as Loser, Name2 as Winner from 
					(select idGame, Winner as idCommand2, CONCAT(Name,' (',City, ')') as Name2 
                    from GameResult natural join Result natural join Command) as a
                    natural join
                    (select idGame, idCommand as idCommand1, CONCAT(Name,' (',City, ')') as Name1 
                    from Game natural join GameCommand natural join Command where
                    not exists (
					select idGame, Winner as idCommand1 from GameResult natural join Result)) as b) as bb;

insert into Place values (1, 'Ukrain', 'Kiev', 'Khreschatik', 8, 2);
insert into Judge values (1, 10, 'Ivan', 'Ivanov', 40, True);

insert into Command Values (1, 'Kiev', 'Dinamo'), (2, 'Moskva', 'Metalurg');
insert into Game values (1, 'friendly', '2017-11-01 10:00:00', 'intresting text about game', 1, 1);
insert into GameCommand values (1, 1, 1);

insert into Result Values (1, 1, '25:15', 1), (2, 2, '25:23', 2), (3, 3, '27:25', 1);
insert into GameResult Values (1, 1, 1), (2, 1, 2), (3, 1, 3);