DROP TABLE `javbus`.`Video`;
DROP TABLE `javbus`.`Magnet`;   


CREATE TABLE IF NOT EXISTS `javbus`.`Magnet` ( 
    `Hash` CHAR(40) NOT NULL, 
    `Magnet` VARCHAR(255) NOT NULL, 
    `Video_ID` VARCHAR(20) NOT NULL, 
    `File_Size` INT(8) NULL, 
    `Share_Date` DATE NULL, 
    `Magnet_Name` TEXT NOT NULL, 
    PRIMARY KEY (`Hash`)) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `javbus`.`Video` ( 
    `Video_ID` VARCHAR(20) NOT NULL, 
    `URL` VARCHAR(255) NOT NULL, 
    `Release_Date` DATE NULL, 
    `Length` INT NULL, 
    `Idol` TEXT NULL, 
    `Studio` VARCHAR(80)  NULL, 
    `Producer` VARCHAR(80)  NULL, 
    `Lable` TEXT NULL, 
    `Censored` BOOLEAN NOT NULL, 
    PRIMARY KEY (`Video_ID`)) ENGINE = InnoDB;

