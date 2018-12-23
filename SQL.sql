INSERT INTO table_listnames (name, address, tele)
SELECT 'Rupert', 'Somewhere', '022'
WHERE NOT EXISTS (SELECT name FROM table_listnames WHERE name = 'Rupert');


INSERT INTO `Video` (`Video_ID`, `URL`, `Release_Date`, `Length`, `Studio`, `Producer`, `Label`, `Censored`) 
SELECT %s,%s,%s,%s,%s,%s,%s,%s
WHERE NOT EXISTS (SELECT `Video_ID` FROM Video WHERE `Video_ID` = %s);
