DROP TABLE `javbus`.`Video`;
DROP TABLE `javbus`.`Actor`;
DROP TABLE `javbus`.`Video_Actor`;
DROP TABLE `javbus`.`Magent`;   


CREATE TABLE IF NOT EXISTS `javbus`.`Magnet` ( 
    `Hash` CHAR(40) NOT NULL, 
    `Magnet` TEXT NOT NULL, 
    `Video_ID` VARCHAR(20) NOT NULL, 
    `File_Size` INT(8) NULL, 
    `Share_Date` DATE NULL, 
    `Magnet_Name` TEXT NOT NULL, 
    `Source` VARCHAR(20),
    PRIMARY KEY (`Hash`)) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `javbus`.`Actor` ( 
    `Name` VARCHAR(80) NOT NULL, 
    PRIMARY KEY (`Name`)) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `javbus`.`Video` ( 
    `Video_ID` VARCHAR(20) NOT NULL, 
    `URL` VARCHAR(255) NOT NULL, 
    `Release_Date` DATE NULL, 
    `Length` INT NULL, 
    `Producer` VARCHAR(80)  NULL, 
    `Series` VARCHAR(80)  NULL, 
    `Label` TEXT NULL, 
    `Censored` BOOLEAN NOT NULL, 
    PRIMARY KEY (`Video_ID`)) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `javbus`.`Video_Actor` ( 
    `Video_ID` VARCHAR(20) NOT NULL, 
    `Actor` VARCHAR(80) NOT NULL, 
    PRIMARY KEY (`Video_ID`,`Actor`)) ENGINE = InnoDB;